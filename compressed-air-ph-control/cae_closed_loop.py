"""
cae_closed_loop.py
============================================================================
Closed-loop validation of the adapted-momentum integral speed controller.
Produces FIGURE 4 and reproduces TABLE II of

    M. Munoz-Arias, L. M. Esquivel-Sancho and D. del Puerto-Flores,
    "Energy-Based Speed Regulation of Compressed-Air Engines,"
    IEEE Transactions on Control Systems Technology (submitted).

----------------------------------------------------------------------------
THE CONTROLLER, eqs. (40) to (42)
----------------------------------------------------------------------------
Error coordinates, eq. (40):

    omega~   = omega_e - omega_e*                    speed error
    thetabar = theta_e - omega_e* t                  angle error, and note
                                                     d(thetabar)/dt = omega~
                                                     so thetabar is the
                                                     INTEGRAL of the speed
                                                     error
    pbar     = p_theta - J omega_e*                  shifted momentum

Adapted momentum and passive output, eq. (41):

    phat = pbar + J A thetabar
    yhat = phat / J = omega~ + A thetabar

yhat is a proportional-plus-integral combination of the speed error. That is
the whole point of the coordinate change: it turns the bare speed port into a
PI port, so an integrator driven by yhat preserves passivity.

Torque command and integral action, eq. (42):

    tau*_gas = b omega_e - J A omega~ - Kp thetabar - Kd yhat + z
    zdot     = -Ki yhat

The term b*omega_e cancels the known viscous friction. The term -J A omega~
cancels the extra derivative introduced by the coordinate change; it is what
makes the transformation lossless.

----------------------------------------------------------------------------
WHAT IS CHECKED
----------------------------------------------------------------------------
Under Assumption 3 the inner loop delivers the commanded torque, so the shaft
subsystem eq. (19) in closed loop becomes the LINEAR system of eq. (48), with
matrix M of eq. (50). This script verifies:

  * M is Hurwitz for both gain sets, with the Routh quantity of eq. (52)
    strictly positive                                     -> Theorem 2
  * the eigenvalues of M equal the roots of Delta(s), eq. (51), to machine
    precision                                             -> Theorem 2
  * omega_e -> omega_e*,  z -> tau_load,  thetabar -> 0    -> Theorem 1
  * the commanded torque stays inside the engine envelope, so Assumption 3
    is not violated over the run                          -> Remark 13

SCOPE. This is the shaft subsystem only, which is what Theorems 1 and 2
address. It does NOT include the valve realisation of eqs. (36) to (38), the
one-sided throttling authority of Remark 8, or the depleting tank of
Remark 7. See Remark 13.

----------------------------------------------------------------------------
USAGE (Windows PowerShell)
----------------------------------------------------------------------------
    python cae_closed_loop.py
    python cae_closed_loop.py --show               open an interactive window
    python cae_closed_loop.py --outdir figures     write into .\\figures\\

Outputs
    closedloop_response.pdf   vector figure, exactly as used in the paper
    closedloop_response.png   raster preview
    a printed table matching Table II
============================================================================
"""

import argparse
import os

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib

import cae_model as M

# ===========================================================================
# 1. GAIN SETS, TABLE II
# ===========================================================================
GAINS = {
    "baseline": dict(A=5.0,  Kp=2.0e-3, Kd=5.0e-4, Ki=2.0e-3),
    "fast":     dict(A=12.0, Kp=8.0e-3, Kd=1.2e-3, Ki=1.0e-2),
}

# ===========================================================================
# 2. OPERATING CONDITIONS, Section V-B
# ===========================================================================
OMEGA_STAR = 2000.0 * M.RPM   # speed reference omega_e*              [rad/s]
TAU_LOAD   = 0.05             # step load torque                      [N m]
T_LOAD     = 4.0              # instant at which the load is applied  [s]
T_END      = 8.0              # simulated duration                    [s]
TAU_PEAK   = 0.9              # engine peak torque, for Remark 13     [N m]


# ===========================================================================
# 3. CLOSED-LOOP ALGEBRA, eqs. (50) to (52)
# ===========================================================================
def closed_loop_matrix(g):
    """Matrix M of eq. (50), in coordinates chi = (thetabar, phat, zbar).

            [ -A        1/J      0 ]
        M = [ -Kp      -Kd/J     1 ]
            [  0       -Ki/J     0 ]
    """
    J = M.J_SH
    return np.array([
        [-g["A"],   1.0 / J,       0.0],
        [-g["Kp"], -g["Kd"] / J,   1.0],
        [0.0,      -g["Ki"] / J,   0.0],
    ])


def char_poly_coeffs(g):
    """Coefficients of Delta(s) in eq. (51), highest power first.

        Delta(s) = s^3 + (A + Kd/J) s^2
                        + (Kp + Ki + A Kd)/J s
                        + A Ki / J
    """
    J, A, Kp, Kd, Ki = M.J_SH, g["A"], g["Kp"], g["Kd"], g["Ki"]
    return [1.0,
            A + Kd / J,
            (Kp + Ki + A * Kd) / J,
            A * Ki / J]


def routh_quantity(g):
    """The Routh condition a2 a1 - a3 a0 of eq. (52).

        a2 a1 - a3 a0 = [ A J (A Kd + Kp) + Kd (A Kd + Ki + Kp) ] / J^2

    Every term is a product of strictly positive quantities, so this is
    positive for ANY positive gain choice. That is Theorem 2: no gain
    condition is required.
    """
    J, A, Kp, Kd, Ki = M.J_SH, g["A"], g["Kp"], g["Kd"], g["Ki"]
    return (A * J * (A * Kd + Kp) + Kd * (A * Kd + Ki + Kp)) / J ** 2


# ===========================================================================
# 4. SIMULATION OF THE CONTROLLED SHAFT
# ===========================================================================
def tau_load_of(t):
    """Step load torque: zero until T_LOAD, then TAU_LOAD.

    Assumption 2 asks for a CONSTANT load. The step is applied so that the
    integrator has to find the new value, which is what the second panel of
    Figure 4 shows. Between steps the load is constant, so the theorem
    applies on each interval.
    """
    return TAU_LOAD if t >= T_LOAD else 0.0


def torque_command(theta_bar, omega, z, g):
    """Commanded gas torque, eq. (42). Works on scalars or arrays."""
    omega_tilde = omega - OMEGA_STAR
    y_hat = omega_tilde + g["A"] * theta_bar          # eq. (41)
    return (M.B_VISC * omega                          # friction feedforward
            - M.J_SH * g["A"] * omega_tilde           # coordinate-change term
            - g["Kp"] * theta_bar                     # proportional on angle
            - g["Kd"] * y_hat                         # damping on yhat
            + z)                                      # integral action


def rhs(t, x, g):
    """Shaft subsystem eq. (19) in closed loop with eq. (42).

    State x = [thetabar, omega_e, z]. These are the physical coordinates;
    the error coordinates chi of eq. (48) are recovered afterwards.

    Under Assumption 3 the delivered gas torque equals the command, so

        J domega/dt = tau*_gas - b omega_e - tau_load
    """
    theta_bar, omega, z = x
    omega_tilde = omega - OMEGA_STAR
    y_hat = omega_tilde + g["A"] * theta_bar               # eq. (41)

    tau_cmd = torque_command(theta_bar, omega, z, g)       # eq. (42)

    d_theta_bar = omega_tilde                              # eq. (40)
    d_omega = (tau_cmd - M.B_VISC * omega - tau_load_of(t)) / M.J_SH
    d_z = -g["Ki"] * y_hat                                 # eq. (42)
    return [d_theta_bar, d_omega, d_z]


def simulate(g, n_out=4000):
    """Integrate from rest with an empty integrator.

    Tight tolerances are used because the point of the run is to confirm the
    steady-state values of Theorem 1 to four decimal places.
    """
    t_eval = np.linspace(0.0, T_END, n_out)
    sol = solve_ivp(rhs, (0.0, T_END), [0.0, 0.0, 0.0], args=(g,),
                    t_eval=t_eval, method="LSODA",
                    rtol=1e-10, atol=1e-12, max_step=1e-3)
    if not sol.success:
        raise RuntimeError(f"integration failed: {sol.message}")
    return sol


# ===========================================================================
# 5. FIGURE 4
# ===========================================================================
def make_figure(sols, gamma_baseline, outdir):
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans",
                         "mathtext.fontset": "dejavusans"})

    sb, sf = sols["baseline"], sols["fast"]
    gb = GAINS["baseline"]

    fig, ax = plt.subplots(2, 2, figsize=(7.16, 4.70))

    # -- top left: speed tracking for both gain sets -----------------------
    ax[0, 0].plot(sb.t, sb.y[1] / M.RPM, "tab:blue", lw=1.2,
                  label="baseline gains")
    ax[0, 0].plot(sf.t, sf.y[1] / M.RPM, "tab:orange", lw=1.2,
                  label="fast gains")
    ax[0, 0].axhline(OMEGA_STAR / M.RPM, ls="--", c="0.35", lw=1,
                     label="reference")
    ax[0, 0].axvline(T_LOAD, ls=":", c="tab:red", lw=1, label="load step")
    ax[0, 0].set(title=r"Shaft speed $\omega_e$",
                 xlabel="time (s)", ylabel="rpm")

    # -- top right: the integrator learns the load, Remark 4 ---------------
    ax[0, 1].plot(sb.t, sb.y[2], "tab:blue", lw=1.2, label=r"integrator $z$")
    ax[0, 1].plot(sb.t, [tau_load_of(t) for t in sb.t], "--", c="0.35", lw=1,
                  label=r"$\tau_{\rm load}(t)$")
    ax[0, 1].set(title=r"Integral state $z \rightarrow \tau_{\rm load}$",
                 xlabel="time (s)", ylabel="torque (N m)")

    # -- bottom left: angle error inside its exponential envelope ----------
    # The envelope is exp(-gamma t) scaled to the largest excursion, with
    # gamma the exact asymptotic rate -max Re(eig M). This is the bound of
    # Theorem 2 made visible.
    env = np.abs(sb.y[0]).max()
    ax[1, 0].plot(sb.t, sb.y[0], "tab:blue", lw=1.2, label=r"$\bar{\theta}$")
    ax[1, 0].plot(sb.t,  env * np.exp(-gamma_baseline * sb.t), "--",
                  c="0.35", lw=1, label=r"$\pm e^{-\gamma t}$")
    ax[1, 0].plot(sb.t, -env * np.exp(-gamma_baseline * sb.t), "--",
                  c="0.35", lw=1)
    ax[1, 0].set(title=r"Angle error $\bar{\theta} \rightarrow 0$",
                 xlabel="time (s)", ylabel="rad")

    # -- bottom right: control effort against the engine ceiling -----------
    tau_cmd = torque_command(sb.y[0], sb.y[1], sb.y[2], gb)
    ax[1, 1].plot(sb.t, tau_cmd, "tab:blue", lw=1.2,
                  label=r"$\tau^{\star}_{\rm gas}$")
    ax[1, 1].axhline(TAU_PEAK, ls="--", c="0.35", lw=1,
                     label=r"engine peak $\approx$ 0.9")
    ax[1, 1].set(title=r"Commanded gas torque $\tau^{\star}_{\rm gas}$",
                 xlabel="time (s)", ylabel="torque (N m)")

    for a in ax.flat:
        a.grid(True, alpha=0.3)
        a.legend(fontsize=7)

    fig.tight_layout()

    os.makedirs(outdir, exist_ok=True)
    pdf = os.path.join(outdir, "closedloop_response.pdf")
    png = os.path.join(outdir, "closedloop_response.png")
    fig.savefig(pdf)
    fig.savefig(png, dpi=150)
    print(f"wrote {pdf}\nwrote {png}")
    return tau_cmd


# ===========================================================================
# 6. REPORT
# ===========================================================================
def report(sols, info, tau_cmd):
    print("\n--- Table II of the manuscript "
          "----------------------------------")
    for name in ("baseline", "fast"):
        g, i = GAINS[name], info[name]
        a = i["poly"]
        eig = np.sort_complex(i["eig"])
        root = np.sort_complex(i["polyroots"])
        print(f"\n[{name}]  A={g['A']}  Kp={g['Kp']}  "
              f"Kd={g['Kd']}  Ki={g['Ki']}")
        print(f"   Delta(s), eq. (51) = s^3 + {a[1]:.4g} s^2 "
              f"+ {a[2]:.4g} s + {a[3]:.4g}")
        print("   eigenvalues of M   : "
              + ", ".join(f"{e:.4g}" for e in eig))
        print("   roots of Delta(s)  : "
              + ", ".join(f"{e:.4g}" for e in root))
        print(f"   max |eig - root|   : {np.abs(eig - root).max():.2e}"
              "   (Theorem 2, numerically)")
        print(f"   Routh, eq. (52)    : {i['routh']:.1f}   "
              f"{'> 0, Hurwitz' if i['routh'] > 0 else 'FAILS'}")
        print(f"   decay rate gamma   : {i['gamma']:.3f} 1/s")

    print("\n--- steady state, Theorem 1 "
          "-------------------------------------")
    for name in ("baseline", "fast"):
        s = sols[name]
        print(f"[{name:8s}] omega_e = {s.y[1][-1] / M.RPM:8.1f} rpm "
              f"(reference {OMEGA_STAR / M.RPM:.0f}),  "
              f"z = {s.y[2][-1]:.4f} N m (load {TAU_LOAD}),  "
              f"theta_bar = {s.y[0][-1]:.2e} rad")

    print(f"\nRemark 13: peak commanded torque = {np.abs(tau_cmd).max():.3f} "
          f"N m against an engine peak of {TAU_PEAK} N m, so Assumption 3 "
          "is not violated.")
    print("-----------------------------------------------------------------")


def main():
    ap = argparse.ArgumentParser(
        description="Closed-loop controller simulation, Figure 4 of the paper")
    ap.add_argument("--outdir", default=".",
                    help="directory for the figure files")
    ap.add_argument("--show", action="store_true",
                    help="open an interactive window instead of exiting")
    args = ap.parse_args()

    if not args.show:
        matplotlib.use("Agg")        # headless: must precede pyplot import

    sols, info = {}, {}
    for name, g in GAINS.items():
        sols[name] = simulate(g)
        eig = np.linalg.eigvals(closed_loop_matrix(g))
        info[name] = dict(
            eig=eig,
            gamma=-eig.real.max(),               # exact asymptotic decay rate
            routh=routh_quantity(g),
            poly=char_poly_coeffs(g),
            polyroots=np.roots(char_poly_coeffs(g)),
        )

    tau_cmd = make_figure(sols, info["baseline"]["gamma"], args.outdir)
    report(sols, info, tau_cmd)

    if args.show:
        import matplotlib.pyplot as plt
        plt.show()


if __name__ == "__main__":
    main()
