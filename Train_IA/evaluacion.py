# evaluacion.py

import numpy as np


def revertir_escala_targets(y_escalado, scaler, config_entrenamiento):
    """
    y_escalado: array (muestras, horizon, n_targets) en escala [0,1]
    Devuelve: array de la misma forma, en unidades fisicas reales
    """
    n_muestras, horizon, n_targets = y_escalado.shape
    columnas_totales = (
        config_entrenamiento["columnas_agregacion_media"]
        + config_entrenamiento["columnas_agregacion_max"]
    )
    n_features_totales = len(columnas_totales)

    # Aplanar a 2D para que el scaler lo acepte: (muestras*horizon, n_targets)
    y_plano = y_escalado.reshape(-1, n_targets)

    relleno = np.zeros((y_plano.shape[0], n_features_totales - n_targets))
    y_plano_completo = np.hstack([y_plano, relleno])

    y_real_completo = scaler.inverse_transform(y_plano_completo)
    y_real = y_real_completo[:, :n_targets]

    return y_real.reshape(n_muestras, horizon, n_targets)


def evaluar_en_test(modelo, X_test, y_test, scaler, config_entrenamiento):
    print("Evaluando en TEST (nunca visto por el modelo)...")
    resultados = modelo.evaluate(X_test, y_test, verbose=0)
    print(f"  loss (MSE, escala [0,1]): {resultados[0]:.5f}")
    print(f"  MAE  (escala [0,1]):      {resultados[1]:.5f}")

    predicciones_escaladas = modelo.predict(X_test, verbose=0)
    predicciones_reales = revertir_escala_targets(
        predicciones_escaladas, scaler, config_entrenamiento
    )
    y_test_reales = revertir_escala_targets(
        y_test, scaler, config_entrenamiento
    )

    targets = config_entrenamiento["targets"]
    print("\nMAE por variable, en unidades fisicas reales:")
    for i, nombre in enumerate(targets):
        mae_real = np.mean(np.abs(
            predicciones_reales[:, :, i] - y_test_reales[:, :, i]
        ))
        unidad = "°C" if nombre == "temp_ambiente" else "%"
        print(f"  {nombre}: {mae_real:.3f} {unidad}")

    return predicciones_reales, y_test_reales