function abrirFormulario() {
    document.getElementById("modal-form").style.display = "flex"; 
} // hace visible el formulario emergente 

function cerrarFormulario() {
    document.getElementById("modal-form").style.display = "none";

}  // oculta el formulario 
//permite que el usuario haga clic en “+ Registrar salida” y vea el formulario.

document.getElementById("form-salida").addEventListener("submit", function (e) {
    e.preventDefault();

    //Aquí detectamos cuando el usuario presiona "Guardar". e.prevent.. evita que la página se recargue.

    // Obtener datos
    const fecha = this.fecha.value;
    const codigo = this.codigo.value;
    const nombre = this.nombre.value;
    const cantidad = this.cantidad.value;
    const motivo = this.motivo.value;
    const responsable = this.responsable.value;

    //Aquí recuperamos los datos ingresados por el usuario. this se refiere al formulario.

    // Insertar en tabla
    const tbody = document.querySelector("#tabla-registros tbody");
    const fila = document.createElement("tr");
    fila.innerHTML = `
        <td>${fecha}</td>
        <td>${codigo}</td>
        <td>${nombre}</td>
        <td>${cantidad}</td>
        <td>${motivo}</td>
        <td>${responsable}</td>
    `;

    // Creamos un elemento <tr> (fila). Rellenamos sus celdas <td> con los valores.

    
    tbody.appendChild(fila);
// Lo añadimos al final de la tabla para que se vea como un nuevo registro.

    // Cerrar formulario
    cerrarFormulario();

    // Mostrar mensaje de éxito
    const mensaje = document.getElementById("mensaje-exito");
    mensaje.style.display = "block";
    setTimeout(() => mensaje.style.display = "none", 3000);

    // Limpiar formulario
    this.reset();
});
