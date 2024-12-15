function flipCard() {
    const flipper = document.querySelector('.flipper');
    flipper.classList.toggle('flipped');
}

function printCV() {
    // Open the PDF in a new tab
    var printWindow = window.open('/static/CurriculumVitae.pdf', '_blank');
    // Wait for the PDF to load and then trigger the print dialog
    printWindow.onload = function() {
        printWindow.print();
    };
}