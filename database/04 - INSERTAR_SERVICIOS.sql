-- =========================================================
-- INSERTS PARA LA TABLA: servicios (Enfoque en Combos)
-- =========================================================

INSERT INTO servicios (
    nombre_servicio, 
    precio_servicio, 
    duracion_minutos, 
    descripcion_servicio
) VALUES 
-- ---------------------------------------------------------
-- COMBOS PRINCIPALES
-- ---------------------------------------------------------
(
    'Combo Básico (Corte + Cejas)', 
    32000.00, 
    45, 
    'Corte de cabello a elección más perfilado de cejas con navaja'
),
(
    'Combo Barbero (Corte + Barba)', 
    45000.00, 
    60, 
    'Corte de cabello moderno o tradicional más perfilado de barba con toalla caliente'
),
(
    'Combo Premium (Corte + Barba + Cejas)', 
    52000.00,
    70, 
    'Servicio completo de corte, arreglo de barba y diseño de cejas'
),
(
    'Combo VIP (Corte + Barba + Mascarilla)', 
    65000.00, 
    80, 
    'Corte, barba, cejas y mascarilla facial de carbón activado'
),
(
    'Combo Padre e Hijo', 
    50000.00, 
    60, 
    'Dos cortes de cabello tradicionales o modernos en la misma sesión'
),
(
    'Combo Express (Barba + Cejas)', 
    25000.00, 
    30, 
    'Perfilado de barba y limpieza de cejas para retoque rápido'
),

-- ---------------------------------------------------------
-- SERVICIOS INDIVIDUALES Y ADICIONALES
-- ---------------------------------------------------------
(
    'Corte Individual', 
    28000.00, 
    35, 
    'Corte de cabello tradicional o degradado (Fade)'
),
(
    'Arreglo de Barba Individual',
    20000.00, 
    30, 
    'Perfilado e hidratación de barba'
),
(
    'Camuflaje de Canas (Adicional)', 
    30000.00, 
    25, 
    'Pigmentación rápida para barba o cabello'
),
(
    'Limpieza Facial (Adicional)', 
    22000.00, 
    20, 
    'Exfoliación e hidratación rápida'
);