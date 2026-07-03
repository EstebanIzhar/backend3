import { useEffect, useState } from "react";
import "./PlatilloForm.css";

function PlatilloForm({ onSubmit, editing }) {
  const [form, setForm] = useState({
    nombre: "",
    descripcion: "",
    categoria: "",
    precio: "",
    disponible: true,
    imagen: "",
  });

  useEffect(() => {
    if (editing) {
      setForm(editing);
    }
  }, [editing]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);

    if (!editing) {
      setForm({
        nombre: "",
        descripcion: "",
        categoria: "",
        precio: "",
        disponible: true,
        imagen: "",
      });
    }
  };

  return (
    <div className="form-container">

      <h2>
        {editing ? "Editar Platillo" : "Registrar Platillo"}
      </h2>

      <form className="platillo-form" onSubmit={handleSubmit}>

        <div className="input-group">
          <label>Nombre</label>
          <input
            type="text"
            name="nombre"
            value={form.nombre}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <label>Descripción</label>
          <textarea
            name="descripcion"
            rows="3"
            value={form.descripcion}
            onChange={handleChange}
            required
          />
        </div>

        <div className="fila">

          <div className="input-group">
            <label>Categoría</label>
            <input
              type="text"
              name="categoria"
              value={form.categoria}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>Precio</label>
            <input
              type="number"
              step="0.01"
              name="precio"
              value={form.precio}
              onChange={handleChange}
              required
            />
          </div>

        </div>

        <div className="input-group">
          <label>URL Imagen</label>
          <input
            type="text"
            name="imagen"
            value={form.imagen}
            onChange={handleChange}
            required
          />
        </div>

        <div className="checkbox">
          <input
            type="checkbox"
            name="disponible"
            checked={form.disponible}
            onChange={handleChange}
          />
          <label>Disponible</label>
        </div>

        <button type="submit">
          {editing ? "Actualizar Platillo" : "Agregar Platillo"}
        </button>

      </form>

    </div>
  );
}

export default PlatilloForm;