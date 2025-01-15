document.addEventListener("DOMContentLoaded", function() {
    const editarItem = document.querySelector(".dropdown .item.transparent");
    const excluirItem = document.querySelector(".dropdown .item.red");
    const botaoSalvar = document.querySelector(".button-salvar");
    const botaoDescartar = document.querySelector(".button-descartar");
    const overlayExcluir = document.getElementById("overlay-excluir");
    const botaoConfirmarExclusao = document.querySelector(".button-confirmar-exclusao");
    const botaoCancelarExclusao = document.querySelector(".button-cancelar-exclusao");
    const dropdownSelected = document.querySelector(".dropdown .selected");
    const dropdownCaret = document.querySelector(".dropdown .caret");

    editarItem.addEventListener("click", function() {
        botaoSalvar.classList.remove("hidden");
        botaoDescartar.classList.remove("hidden");
        overlayExcluir.classList.add("hidden");
        dropdownSelected.textContent = "Alterar solicitação";
    });

    excluirItem.addEventListener("click", function() {
        botaoSalvar.classList.add("hidden");
        botaoDescartar.classList.add("hidden");
        overlayExcluir.classList.remove("hidden");
        dropdownSelected.textContent = "Excluir solicitação"; // Mudar o texto para "Excluir solicitação"
    });

    // Se o usuário confirmar a exclusão
    botaoConfirmarExclusao.addEventListener("click", function() {
        alert("Solicitação excluída!");
        location.reload()
    });

    // Se o usuário cancelar a exclusão
    botaoCancelarExclusao.addEventListener("click", function() {
        overlayExcluir.classList.add("hidden");
        dropdownSelected.textContent = "Alterar solicitação";
    });

    // Se o usuário clicar em "Salvar" (após editar)
    botaoSalvar.addEventListener("click", function() {
        alert("Alterações salvas!");
        location.reload()
    });

    // Se o usuário clicar em "Descartar alterações"
    botaoDescartar.addEventListener("click", function() {
        botaoSalvar.classList.add("hidden");
        botaoDescartar.classList.add("hidden");
        dropdownSelected.textContent = "Alterar solicitação";
    });
});
