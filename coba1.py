import numpy as np
from sklearn.metrics import confusion_matrix

data = np.array([
    [65, 20], [60, 22], [55, 23],
    [58, 24], [62, 21], [59, 25],

    [95, 10], [100, 8], [90, 11],
    [92, 9], [97, 12], [93, 10]
])

labels = np.array([0]*6 + [1]*6)

X0 = data[labels == 0]
X1 = data[labels == 1]

mu0 = np.mean(X0, axis=0)   # mean kelas 0
mu1 = np.mean(X1, axis=0)   # mean kelas 1

P0 = len(X0) / len(data)    # prior kelas 0
P1 = len(X1) / len(data)    # prior kelas 1

cov0 = np.cov(X0, rowvar=False, bias=True)
cov1 = np.cov(X1, rowvar=False, bias=True)

Sw = cov0 * len(X0) + cov1 * len(X1)
Sw /= (len(X0) + len(X1))

Sw_inv = np.linalg.inv(Sw)

def discriminant(x, mu, prior):
    term1 = mu @ Sw_inv @ x.T
    term2 = -0.5 * mu @ Sw_inv @ mu.T
    term3 = np.log(prior)
    return term1 + term2 + term3

predictions = []

for x in data:
    f0 = discriminant(x, mu0, P0)
    f1 = discriminant(x, mu1, P1)
    predicted = 0 if f0 > f1 else 1
    predictions.append(predicted)

predictions = np.array(predictions)

accuracy = np.mean(predictions == labels)
tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)

print("=== MEAN PER KELAS ===")
print(f"Mean Autisme Berat (0): {mu0}")
print(f"Mean Autisme Ringan (1): {mu1}\n")

print("=== PRIOR PROBABILITAS ===")
print(f"P(Kelas 0): {P0:.2f}")
print(f"P(Kelas 1): {P1:.2f}\n")

print("=== FUNGSI DISKRIMINAN ===")
print("f(x) = μ.T @ C^(-1) @ x - ½ μ.T @ C^(-1) @ μ + ln(P)")
print("Threshold: jika f1 > f0 → Kelas 1 (Ringan), else Kelas 0 (Berat)\n")

print("=== EVALUASI MODEL ===")
print(f"Accuracy     : {accuracy:.2%}")
print(f"Sensitivity  : {sensitivity:.2%}")
print(f"Specificity  : {specificity:.2%}")


def klasifikasi_autisme():
    print("\nMasukkan data pengguna:")
    try:
        iq = float(input("IQ: "))
        ados = float(input("Skor ADOS: "))
    except ValueError:
        print("Input tidak valid.")
        return

    x = np.array([iq, ados])
    f0 = discriminant(x, mu0, P0)
    f1 = discriminant(x, mu1, P1)

    print("\n=== HASIL KLASIFIKASI ===")
    print(f"f0 (Autisme Berat) : {f0:.4f}")
    print(f"f1 (Autisme Ringan): {f1:.4f}")

    if f1 > f0:
        print("Hasil: Autisme Ringan (Kelas 1)")
    else:
        print("Hasil: Autisme Berat (Kelas 0)")

klasifikasi_autisme()
