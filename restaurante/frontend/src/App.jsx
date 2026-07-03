import { useEffect, useState } from "react";
import "./App.css";
import api from "./services/api";
import PlatilloCard from "./components/PlatilloCard";
import PlatilloForm from "./components/PlatilloForm";

function App() {
  const [platillos, setPlatillos] = useState([]);
  const [editing, setEditing] = useState(null);

  useEffect(() => {
    obtenerPlatillos();
  }, []);

  const obtenerPlatillos = async () => {
    const res = await api.get("platillos/");
    setPlatillos(res.data);
  };

  const guardarPlatillo = async (platillo) => {
    if (editing) {
      await api.put(`platillos/${editing.id}/`, platillo);
      setEditing(null);
    } else {
      await api.post("platillos/", platillo);
    }

    obtenerPlatillos();
  };

  const eliminarPlatillo = async (id) => {
    const confirmar = window.confirm("¿Seguro que deseas eliminar?");
    if (!confirmar) return;

    await api.delete(`platillos/${id}/`);
    obtenerPlatillos();
  };

  const cambiarDisponibilidad = async (platillo) => {
    await api.put(`platillos/${platillo.id}/`, {
      ...platillo,
      disponible: !platillo.disponible,
    });

    obtenerPlatillos();
  };

  return (
    <div className="container">

      <header>
        <h1>Sistema de Restaurante</h1>
        <p>Gestión de menú digital</p>
      </header>

      <PlatilloForm
        onSubmit={guardarPlatillo}
        editing={editing}
      />

      <h2 className="titulo-menu">
        Catálogo de Platillos ({platillos.length})
      </h2>

      <div className="contenedor-platillos">

        {platillos.map((platillo) => (
          <PlatilloCard
            key={platillo.id}
            platillo={platillo}
            onEdit={setEditing}
            onDelete={eliminarPlatillo}
            onChangeAvailability={cambiarDisponibilidad}
          />
        ))}

      </div>

    </div>
  );
}

export default App;