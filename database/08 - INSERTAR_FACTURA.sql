-- =========================================================
-- TABLA: factura
-- Asociados a las citas creadas para CL001 y CL004
-- =========================================================

-- FACTURA PARA LA CITA 1 (Subtotal: $45.000, IVA 19%: $8.550, Total: $53.550)
INSERT INTO Factura (
    fecha_factura,
    subtotal_factura,
    iva_factura,
    total_factura,
    estado_factura,
    metodo_pago_factura
) VALUES (
    NOW(),
    45000.00,
    8550.00,
    53550.00,
    'pagada',
    'efectivo'
);

-- FACTURA PARA LA CITA 2 (Subtotal: $25.000, IVA 19%: $4.750, Total: $29.750)
INSERT INTO Factura (
    fecha_factura,
    subtotal_factura,
    iva_factura,
    total_factura,
    estado_factura,
    metodo_pago_factura
) VALUES (
    NOW(),
    25000.00,
    4750.00,
    29750.00,
    'pagada',
    'transferencia'
);
