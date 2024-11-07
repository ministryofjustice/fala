const printResultsPage = document.getElementById("printButton");

if (printResultsPage) {
  printResultsPage.addEventListener("click", () => {
    window.print();
  })
};

