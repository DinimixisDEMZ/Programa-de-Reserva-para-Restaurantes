# 📝 Reservaciones

Esta app permite gestionar reservas de mesas en un restaurante desde una interfaz web amigable y dinámica.

## Funcionalidades

- Mostrar mesas por ubicación y estado (disponible, ocupada, reservada)
- Crear reservas filtrando por número de huéspedes
- Actualización en tiempo real sin recargar la página ##No funcional 
- Integración con Django Admin y API personalizada

## Vistas disponibles

- `reservaciones_page`: renderiza el frontend principal
- `api_create_reservation`: guarda nuevas reservas (POST)
- `api_estado`: devuelve mesas y reservas actualizadas (GET)

## Modelos relacionados

- `Table`: define cada mesa con capacidad, ubicación y estado
- `Reservation`: representa cada reserva con cliente, fecha, hora y mesa asociada

## Requisitos

- Django 4+
- Bootstrap (opcional para estilos)
- Activar Django Admin con superusuario

## Próximas mejoras

- Edición y cancelación de reservas
- Filtrado por fecha futura
- Panel administrativo personalizado
