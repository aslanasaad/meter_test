import numpy as np

def calculate_symmetrical_components(phase_values):
    """
    Calculates the positive, negative, and zero sequence components of a set of three-phase values.

    Args:
        phase_values: A list or array containing the three phase values (e.g., [V_a, V_b, V_c]).

    Returns:
        A list containing the positive sequence component, negative sequence component, and zero sequence component.
    """

    alpha = np.exp(2j * np.pi / 3)  # Complex number representing 120 degree phase shift

    # Transformation matrix
    T = np.array([[1, 1, 1], [1, alpha, alpha ** 2], [1, alpha ** 2, alpha]]) / 3

    # Calculate symmetrical components
    symmetrical_components = np.dot(T, phase_values)

    # Round very small values to zero for better readability
    symmetrical_components = np.round(symmetrical_components, decimals=10)

    return symmetrical_components

# Correct phase voltages for a balanced system
V_a = 10  # Phase A, 100V at 0 degrees
V_b = -10+0j
V_c = 0   # Phase C, 100V at +120 degrees

phase_voltages = [V_a, V_b, V_c]
positive_seq, negative_seq, zero_seq = calculate_symmetrical_components(phase_voltages)

print("Positive sequence:", positive_seq)
print("Negative sequence:", negative_seq)
print("Zero sequence:", zero_seq)
