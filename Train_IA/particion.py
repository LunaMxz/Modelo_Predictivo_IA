# particion.py

def dividir_cronologico(df_15min, config_entrenamiento):
    proporciones = config_entrenamiento["split"]
    suma = sum(proporciones.values())
    if abs(suma - 1.0) > 1e-6:
        raise ValueError(
            f"Las proporciones de split deben sumar 1.0, suman {suma}. "
            f"Revisa config_entrenamiento['split']."
        )

    n = len(df_15min)
    n_train = int(n * proporciones["train"])
    n_val = int(n * proporciones["val"])

    train = df_15min.iloc[:n_train]
    val = df_15min.iloc[n_train:n_train + n_val]
    test = df_15min.iloc[n_train + n_val:]

    print(f"Train: {len(train)} filas  ({train.index.min()} a {train.index.max()})")
    print(f"Val:   {len(val)} filas  ({val.index.min()} a {val.index.max()})")
    print(f"Test:  {len(test)} filas  ({test.index.min()} a {test.index.max()})")

    return train, val, test