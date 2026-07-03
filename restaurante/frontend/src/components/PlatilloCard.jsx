import "./PlatilloCard.css";

function PlatilloCard({
  platillo,
  onEdit,
  onDelete,
  onChangeAvailability,
}) {
  return (
    <div className="platillo-seccion">

      <div className="platillo-img-wrap">
        <img
          src={platillo.imagen}
          alt={platillo.nombre}
          className="platillo-img"
        />
      </div>

      <div className="platillo-info">

        <div className="platillo-header">
          <h2>{platillo.nombre}</h2>
          <span className="categoria">{platillo.categoria}</span>
        </div>

        <p className="descripcion">{platillo.descripcion}</p>

        <div className="platillo-footer">
          <h3 className="precio">
            ${Number(platillo.precio).toFixed(2)}
          </h3>

          <p
            className={
              platillo.disponible
                ? "estado disponible"
                : "estado nodisponible"
            }
          >
            {platillo.disponible ? "Disponible" : "No Disponible"}
          </p>
        </div>

        <div className="botones">
          <button className="editar" onClick={() => onEdit(platillo)}>
            Editar
          </button>

          <button className="eliminar" onClick={() => onDelete(platillo.id)}>
            Eliminar
          </button>

          <button
            className="disponibilidad"
            onClick={() => onChangeAvailability(platillo)}
          >
             Cambiar Estado
          </button>
        </div>

      </div>

    </div>
  );
}

export default PlatilloCard;