"""
cae_model.py
============================================================================
Shared parameters and dynamics for the compressed-air Wankel drive-train.

    M. Munoz-Arias, L. M. Esquivel-Sancho and D. del Puerto-Flores,
    "Energy-Based Speed Regulation of Compressed-Air Engines,"
    IEEE Transactions on Control Systems Technology (submitted).

This module holds the physics and nothing else. It draws no figures and has
no side effects on import. The two runnable scripts import it:

    cae_open_loop.py    ->  Figure 3   (Section V-A)
    cae_closed_loop.py  ->  Figure 4   (Section V-B, Table II)

----------------------------------------------------------------------------
MAP FROM THE PAPER TO THIS FILE
----------------------------------------------------------------------------
    Paper                                      Here
    ---------------------------------------    -----------------------------
    (6)   ideal gas law                        R_AIR, T_A, T_0
    (7)   tank capacitance C_1                 C_1
    (9)   pipe inertance I_m                   I_M
    (11)  valve sizing equation                C_V, N_6, Y_EXP
    (12)  normalised opening D                 argument `D` of the rhs
    (13)  orifice constant K_1                 K_1
    (14)  valve resistance R_v(Q_m, D)         inline in three_chamber_rhs
    (15)  chamber volume V(theta_e)            chamber_geometry
    (16)  moment arm alpha(theta_e)            chamber_geometry
    (17)  chamber pressure dynamics            three_chamber_rhs, `dp`
    (18)  gas torque tau_gas = p * alpha       three_chamber_rhs, `tau_gas`
    (19)  shaft dynamics                       three_chamber_rhs, `dp_theta`
    (20)  exhaust mass flow                    exhaust_flow
    (21)  flow function Psi                    psi_flow
    (22)  state vector x                       docstring of three_chamber_rhs
    (26)  dissipation matrix R(x)              K_1/D**2 term and B_VISC
    (31)-(35) explicit state equations         three_chamber_rhs
    Table I  parameters                        the block marked "Table I"

Everything the controller needs lives in cae_closed_loop.py, not here,
because Theorems 1 and 2 act on the shaft subsystem alone.
============================================================================
"""

import numpy as np

# ===========================================================================
# 1. PHYSICAL CONSTANTS
# ===========================================================================
R_AIR = 287.058           # specific gas constant of air            [J/(kg K)]
GAMMA = 1.4               # ratio of specific heats                 [-]
P_ATM = 1.01325e5         # atmospheric pressure                    [Pa]

# Critical pressure ratio below which the exhaust chokes, eq. (21).
PI_CR = (2.0 / (GAMMA + 1.0)) ** (GAMMA / (GAMMA - 1.0))      # ~ 0.528


# ===========================================================================
# 2. TABLE I OF THE PAPER
#
#    These are the reference parameters printed in the manuscript. The one
#    exception is the chamber geometry, which is overridden in section 3
#    below by the measured bench values. See the footnote to Table I.
# ===========================================================================
V_TANK = 1.0e-3           # pressure tank volume                    [m^3] = 1 L
T_A    = 293.0            # tank air temperature                    [K]
T_0    = 293.0            # chamber air temperature                 [K]
C_D    = 0.85             # orifice discharge coefficient           [-]
L_PIPE = 0.4              # main pipe length                        [m]
A_PIPE = 80.0e-6          # pipe cross-sectional area               [m^2]
A_OUT  = 1.0e-6           # exhaust port area                       [m^2]
C_V    = 4.0              # valve flow coefficient                  [-]
N_6    = 7.583e-7         # valve unit constant                     [-]
Y_EXP  = 1.0              # expansion factor Y in eq. (11)          [-]
J_SH   = 1.0e-4           # shaft rotational inertia                [kg m^2]
B_VISC = 1.0e-3           # viscous friction coefficient b          [kg m^2/s]


# ===========================================================================
# 3. MEASURED BENCH GEOMETRY
#
#    Table I lists a mean chamber volume of 0.1 L for the reference geometry.
#    The engine actually on the bench is about twelve times smaller, and it is
#    the measured values below that these simulations use. This is the scale
#    discrepancy discussed in Section V-A and listed as the fourth limitation
#    in Section VII.
# ===========================================================================
V_BAR   = 8.25e-6         # mean chamber volume    V_bar in eq. (15)   [m^3]
DELTA_V = 1.25e-5         # swept chamber volume   DeltaV in eq. (15)  [m^3]


# ===========================================================================
# 4. DERIVED QUANTITIES
# ===========================================================================
# Tank pneumatic capacitance, eq. (7):  C_1 = V_t / (R T_a)
C_1 = V_TANK / (R_AIR * T_A)

# Pipe inertance, eq. (9):  I_m = L / A_p
I_M = L_PIPE / A_PIPE

# Initial charge of the tank. Not a Table I entry; it is the operating
# condition stated in Section V-A.
P1_0 = 6.0e5              # tank charge pressure                    [Pa abs]

# Upstream density at the charge pressure, used in eq. (13).
RHO_IN = P1_0 / (R_AIR * T_A)

# Orifice constant, eq. (13):  K_1 = 1 / (C_v^2 N_6^2 Y^2 rho_in)
K_1 = 1.0 / (C_V ** 2 * N_6 ** 2 * Y_EXP ** 2 * RHO_IN)


# ===========================================================================
# 5. PORT TIMING
#
#    Each chamber is described by its own phase
#
#        psi_i = (2/3) * theta_e - phase_i        modulo 2 pi
#
#    which follows from the rotor kinematics theta_r = theta_e / 3 above
#    eq. (15). Expansion, where alpha > 0, spans psi in (0, pi); compression
#    spans (pi, 2 pi). Air is admitted early in expansion and cut off partway,
#    and the exhaust opens before bottom dead centre and closes near top dead
#    centre.
#
#    CAVEAT. These four angles are NOT calibrated. They are set to physically
#    reasonable values because the port angles of this engine are not
#    documented. The steady speed plateau is sensitive to them, which is the
#    port-timing calibration gap named in Sections V-A and VII. Fitting them
#    to a measured bench trace is the first item of future work.
# ===========================================================================
INTAKE_OPEN   = 0.00 * np.pi     # intake opens just after top dead centre
INTAKE_CUTOFF = 0.55 * np.pi     # intake closes partway through expansion
EXHAUST_OPEN  = 0.90 * np.pi     # exhaust opens before bottom dead centre
EXHAUST_CLOSE = 1.95 * np.pi     # exhaust closes near top dead centre
EPS_PSI       = 0.06 * np.pi     # smoothing width applied to each gate

# Three chambers, evenly spaced 120 degrees apart in the rotor cycle.
PHASE = np.array([0.0, 1.0, 2.0]) * (2.0 * np.pi / 3.0)


def window(psi, lo, hi):
    """Smooth port gate: 1 inside (lo, hi) modulo 2 pi, 0 outside.

    A hard on/off switch makes the flow routing discontinuous and the
    integrator stalls, so each port is opened with a pair of tanh ramps of
    width EPS_PSI. This is a numerical smoothing of the physical port, not a
    modelling assumption.
    """
    psi = np.mod(psi, 2.0 * np.pi)
    opening = 0.5 * (1.0 + np.tanh((psi - lo) / EPS_PSI))
    closing = 0.5 * (1.0 + np.tanh((hi - psi) / EPS_PSI))
    return opening * closing


# ===========================================================================
# 6. CHAMBER GEOMETRY, eqs. (15) and (16)
# ===========================================================================
def chamber_geometry(theta_e):
    """Per-chamber phase, volume and moment arm.

    Implements, for each of the three chambers,

        V(theta_e)     = V_bar - (DeltaV / 2) cos( (2/3) theta_e )      (15)
        alpha(theta_e) = dV/dtheta_e = (DeltaV / 3) sin( (2/3) theta_e ) (16)

    with the per-chamber phase offset of section 5 subtracted.

    Returns
    -------
    psi, V, alpha : ndarray, each of shape (3,)
        Phase [rad], chamber volume [m^3], moment arm [m^3/rad].

    The single scalar alpha carries the entire force geometry of the rotor
    into the dynamics; see the text below eq. (16).
    """
    psi = (2.0 / 3.0) * theta_e - PHASE
    V = V_BAR - 0.5 * DELTA_V * np.cos(psi)
    alpha = (DELTA_V / 3.0) * np.sin(psi)
    return psi, V, alpha


# ===========================================================================
# 7. EXHAUST, eqs. (20) and (21)
# ===========================================================================
def psi_flow(pressure_ratio):
    """Compressible flow function Psi(pi), eq. (21).

    Choked for pi <= PI_CR, subsonic above it. `pressure_ratio` is
    pi = p_e / p, the ratio of downstream to chamber pressure.
    """
    pr = np.clip(pressure_ratio, 1e-9, 1.0)
    if pr <= PI_CR:
        # choked branch: sqrt( gamma * (2/(gamma+1))^((gamma+1)/(gamma-1)) )
        return np.sqrt(GAMMA * (2.0 / (GAMMA + 1.0))
                       ** ((GAMMA + 1.0) / (GAMMA - 1.0)))
    # subsonic branch
    return np.sqrt((2.0 * GAMMA / (GAMMA - 1.0))
                   * (pr ** (2.0 / GAMMA) - pr ** ((GAMMA + 1.0) / GAMMA)))


def exhaust_flow(p_chamber, psi_i):
    """Exhaust mass flow of one chamber, eq. (20).

        mdot_out = C_d A_out (p / sqrt(R T_0)) Psi(pi) * 1_[p > p_e]

    with the indicator of eq. (20) realised by the smooth exhaust port gate
    of section 5, so that the port opens and closes with rotor angle.

    Parameters
    ----------
    p_chamber : float   chamber pressure [Pa abs]
    psi_i     : float   phase of this chamber [rad]

    Returns
    -------
    float : mass flow out of the chamber [kg/s], never negative
    """
    if p_chamber <= P_ATM:
        return 0.0
    gate = window(psi_i, EXHAUST_OPEN, EXHAUST_CLOSE)
    return (C_D * A_OUT * (p_chamber / np.sqrt(R_AIR * T_0))
            * psi_flow(P_ATM / p_chamber) * gate)


# ===========================================================================
# 8. OPEN-LOOP DYNAMICS, eqs. (31) to (35)
# ===========================================================================
def three_chamber_rhs(t, x, D, tau_load=0.0):
    """Right-hand side of the three-chamber open-loop drive-train.

    This is the three-chamber version of the five-state model of eqs. (31)
    to (35). The single chamber of the manuscript becomes three chambers
    sharing one tank and one pipe, so the state is

        x = [ P_1, Q_m, p_1, p_2, p_3, p_theta, theta_e ]           cf. (22)

        P_1       tank pressure                     [Pa abs]
        Q_m       pipe mass flow                    [kg/s]
        p_1..p_3  chamber pressures                 [Pa abs]
        p_theta   shaft angular momentum            [kg m^2/s]
        theta_e   eccentric shaft angle             [rad]

    Parameters
    ----------
    t        : float    time [s], unused, present for solve_ivp
    x        : sequence state as above
    D        : float    normalised valve opening in (0, 1], eq. (12)
    tau_load : float    load torque [N m], zero for the open-loop study

    Returns
    -------
    list : the seven time derivatives

    Note on where the control enters. D appears ONLY in the pipe row below,
    inside the resistance K_1/D^2. It never appears in an input matrix. That
    is the structural gap of Remark 1: the valve modulates dissipation and
    cannot inject energy.
    """
    # ---- unpack -----------------------------------------------------------
    P1, Qm = x[0], x[1]
    p = np.array(x[2:5], dtype=float)
    p_theta, theta_e = x[5], x[6]
    omega = p_theta / J_SH                      # shaft speed, eq. (35)

    psi, V, alpha = chamber_geometry(theta_e)   # eqs. (15), (16)

    # ---- intake routing ---------------------------------------------------
    # Only chambers that are BOTH expanding (alpha > 0) AND have the intake
    # port open receive air. The pipe flow is split among them in proportion
    # to their moment arm, and the back-pressure the pipe sees is the same
    # weighted average. This replaces the single chamber pressure p of
    # eq. (32) with an effective feed pressure.
    w_intake = window(psi, INTAKE_OPEN, INTAKE_CUTOFF)
    a_pos = np.maximum(alpha, 0.0) * w_intake
    a_sum = a_pos.sum()
    if a_sum > 1e-15:
        share = a_pos / a_sum                   # fraction of Q_m per chamber
        p_feed = float((a_pos * p).sum() / a_sum)
    else:
        share = np.zeros(3)                     # all ports shut
        p_feed = float(p.mean())

    # ---- pipe momentum, eq. (32) -----------------------------------------
    #   I_m dQ_m/dt = P_1 - p - (K_1 / D^2) Q_m |Q_m|
    # The last term is the valve, R_v of eq. (14), which sits in the
    # dissipation matrix R(x) of eq. (26).
    dQm = (1.0 / I_M) * (P1 - p_feed - (K_1 / D ** 2) * Qm * abs(Qm))

    # ---- chamber pressures, eq. (33) --------------------------------------
    #   dp/dt = (R T_0 / V)(Q_m - mdot_out) - (p alpha / V) omega
    # First group is filling and emptying, second is the moving-boundary
    # back-action.
    Qm_in = share * Qm
    m_out = np.array([exhaust_flow(p[i], psi[i]) for i in range(3)])
    dp = (R_AIR * T_0 / V) * (Qm_in - m_out) - (p * alpha / V) * omega

    # ---- tank, eq. (31) ---------------------------------------------------
    dP1 = -(1.0 / C_1) * Qm

    # ---- shaft, eq. (34) --------------------------------------------------
    # Gas torque is eq. (18) summed over the three chambers.
    tau_gas = float((p * alpha).sum())
    dp_theta = tau_gas - B_VISC * omega - tau_load

    # ---- angle, eq. (35) --------------------------------------------------
    dtheta_e = omega

    return [dP1, dQm, dp[0], dp[1], dp[2], dp_theta, dtheta_e]


def initial_state():
    """Charged tank, still shaft, chambers at atmospheric.

    The engine self-starts from rest; there is no starter motor in the model.
    """
    return [P1_0, 0.0, P_ATM, P_ATM, P_ATM, 0.0, 0.0]


# ===========================================================================
# 9. UNIT CONVERSIONS USED BY THE FIGURES
# ===========================================================================
RPM = 2.0 * np.pi / 60.0      # rad/s per rpm
BAR = 1.0e5                   # Pa per bar


def mass_to_litre_per_hour(qm):
    """Mass flow [kg/s] -> volumetric flow [L/h] at atmospheric conditions.

    The bench instrument reads volumetric flow at atmospheric conditions, so
    the simulated mass flow is converted the same way before comparison. The
    reference density is P_ATM / (R T_a), not the tank density.
    """
    rho_atm = P_ATM / (R_AIR * T_A)
    return qm / rho_atm * 1000.0 * 3600.0
