-- =========================================================
-- TABLA INTERMEDIA: servicio_disponibilidad
-- Asocia servicios a los bloques de disponibilidad
-- (Usamos las disponibilidades 1 a 15 de los primeros especialistas)
-- =========================================================

INSERT INTO servicio_disponibilidad (id_servicios, id_disponibilidad) VALUES
-- Asocian combos al especialista ES001 el 24-Ago-2026
(2, 1),  -- Combo Barbero en disp #1 (08:00 AM)
(3, 2),  -- Combo Premium en disp #2 (09:00 AM)
(1, 3),  -- Combo Básico en disp #3 (10:00 AM)
(4, 4),  -- Combo VIP en disp #4 (11:00 AM)

-- Asocian combos al especialista ES002 el 24-Ago-2026
(2, 46), -- Combo Barbero en disp #46 (08:00 AM)
(5, 47), -- Combo Padre e Hijo en disp #47 (09:00 AM)
(1, 48), -- Combo Básico en disp #48 (10:00 AM)

-- Asocian combos al especialista ES003 el 24-Ago-2026
(3, 91), -- Combo Premium en disp #91 (08:00 AM)
(6, 92), -- Combo Express en disp #92 (09:00 AM)
(2, 93); -- Combo Barbero en disp #93 (10:00 AM)


