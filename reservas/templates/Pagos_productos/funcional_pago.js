// Esperar a que el DOM se cargue completamente
document.addEventListener('DOMContentLoaded', function() {
    const botones = document.querySelectorAll('.boton-menu');

    botones.forEach(boton => {
        boton.addEventListener('click', function() {
            // Remover la clase 'active' de todos los botones
            botones.forEach(b => b.classList.remove('active'));

            // Añadir la clase 'active' al botón clickeado
            this.classList.add('active');
        });
    });
});
