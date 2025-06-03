import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 299792.458  # speed of light in km/s
H0 = 70  # Hubble constant in km/s/Mpc
Mpc_to_km = 3.0857e19  # 1 Mpc in km

# Function to calculate H(z) based on ΛCDM
def Hubble(z, Omega_m=0.3, Omega_lambda=0.7):
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + Omega_lambda)

# Comoving distance D_C(z)
def comoving_distance(z, Omega_m=0.3, Omega_lambda=0.7):
    dz = 0.0005
    z_array = np.arange(0, z + dz, dz)
    integrand = c / Hubble(z_array, Omega_m, Omega_lambda)
    distance = np.trapz(integrand, z_array)
    return distance  # in Mpc

# Lookback time t_L(z)
def lookback_time(z, Omega_m=0.3, Omega_lambda=0.7):
    dz = 0.0005
    z_array = np.arange(0, z + dz, dz)
    integrand = 1 / ((1 + z_array) * Hubble(z_array, Omega_m, Omega_lambda))
    time_in_sec = np.trapz(integrand, z_array) * Mpc_to_km / c
    time_in_Gyr = time_in_sec / (60 * 60 * 24 * 365.25 * 1e9)
    return time_in_Gyr

# Observed wavelength λ_obs = λ_emitted * (1 + z)
def observed_wavelength(lambda_emitted, z):
    return lambda_emitted * (1 + z)

# Main loop
while True:
    print("\n=== Cosmological Redshift Simulation ===")

    try:
        z = float(input("Enter redshift z (e.g., 1.5): "))
        if z <= 0:
            raise ValueError("Redshift must be > 0.")

        lambda_em = float(input("Enter emitted wavelength in nm (e.g., 121.6 for Lyman-α): "))
        Omega_m = float(input("Enter Omega_m (default 0.3): ") or 0.3)
        Omega_lambda = float(input("Enter Omega_lambda (default 0.7): ") or 0.7)

    except ValueError as e:
        print(f"❌ Invalid input: {e}")
        continue

    # Perform calculations
    lambda_obs = observed_wavelength(lambda_em, z)
    distance = comoving_distance(z, Omega_m, Omega_lambda)
    lookback = lookback_time(z, Omega_m, Omega_lambda)

    # Display results
    print("\n--- Simulation Results ---")
    print(f"Redshift (z)               : {z:.3f}")
    print(f"Emitted Wavelength         : {lambda_em:.2f} nm")
    print(f"Observed Wavelength        : {lambda_obs:.2f} nm")
    print(f"Comoving Distance          : {distance:.2f} Mpc")
    print(f"Light Travel Time (Lookback): {lookback:.2f} Gyr")
    print(f"\nExplanation:")
    print(f"- The universe has expanded by a factor of {1+z:.2f} since this light was emitted.")
    print(f"- Light emitted at {lambda_em:.1f} nm is now observed at {lambda_obs:.1f} nm.")
    print(f"- It took {lookback:.2f} billion years for this light to reach us.")

    # Plotting range
    z_range = np.linspace(0.01, 10, 400)
    lambda_all = observed_wavelength(lambda_em, z_range)
    dist_all = np.array([comoving_distance(zi, Omega_m, Omega_lambda) for zi in z_range])
    lookback_all = np.array([lookback_time(zi, Omega_m, Omega_lambda) for zi in z_range])

    # Plotting
    plt.figure(figsize=(16, 5))

    plt.subplot(1, 3, 1)
    plt.plot(z_range, lambda_all, color='darkred')
    plt.title("Redshift vs Observed Wavelength")
    plt.xlabel("Redshift z")
    plt.ylabel("Observed Wavelength (nm)")
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(z_range, dist_all, color='navy')
    plt.title("Redshift vs Comoving Distance")
    plt.xlabel("Redshift z")
    plt.ylabel("Distance (Mpc)")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(z_range, lookback_all, color='darkgreen')
    plt.title("Redshift vs Lookback Time")
    plt.xlabel("Redshift z")
    plt.ylabel("Lookback Time (Gyr)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Ask to repeat or exit
    again = input("\nDo you want to simulate another redshift? (yes/no): ").lower()
    if again not in ['yes', 'y']:
        print("🔚 Simulation ended. Thank you!")
        break
