// JavaScript code (script.js)

// Get form and input elements
const uploadForm = document.getElementById('upload-form');
const progressBar = document.getElementById('progress-bar');
const statusMessage = document.getElementById('status-message');
const downloadLink = document.getElementById('download-link');

// Add event listener to form submission
uploadForm.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent default form submission

  // Get the selected file
  const fileInput = document.getElementById('documentFile');
  const file = fileInput.files[0];

  try {
    // Display loading message and progress bar
    statusMessage.textContent = 'Converting...';
    progressBar.style.width = '0%';
    progressBar.style.display = 'block';

    // Convert file to PDF
    const pdfBytes = await convertToPDF(file);

    // Create a Blob from the PDF bytes
    const pdfBlob = new Blob([pdfBytes], { type: 'application/pdf' });

    // Generate a temporary download link
    const tempDownloadLink = URL.createObjectURL(pdfBlob);

    // Set the download link href and display it
    downloadLink.href = tempDownloadLink;
    downloadLink.style.display = 'inline';
    downloadLink.download = 'converted.pdf';

    // Update status message
    statusMessage.textContent = 'Conversion completed!';
  } catch (error) {
    // Display error message
    statusMessage.textContent = 'Conversion failed. Please try again.';
    console.error(error);
  } finally {
    // Hide progress bar
    progressBar.style.display = 'none';
  }
});

// Function to convert file to PDF using pdf-lib
async function convertToPDF(file) {
  const fileData = await readFileAsArrayBuffer(file);
  const fileType = file.type;

  // Load the PDFLib library
  await PDFLib.load();

  // Create a new PDF document
  const pdfDoc = await PDFLib.PDFDocument.create();

  // Embed the file into the PDF based on its type
  if (fileType.startsWith('image/')) {
    const embeddedImage = await pdfDoc.embedJpg(fileData);
    const imagePage = pdfDoc.addPage();
    imagePage.drawImage(embeddedImage, {
      x: 0,
      y: 0,
      width: imagePage.getWidth(),
      height: imagePage.getHeight(),
    });
  } else {
    const embeddedDocument = await pdfDoc.embedDocument(fileData);
    const documentPages = await pdfDoc.copyPages(embeddedDocument, embeddedDocument.getPageIndices());
    documentPages.forEach((page) => pdfDoc.addPage(page));
  }

  // Generate the final PDF document as array buffer
  const pdfBytes = await pdfDoc.save();

  return pdfBytes;
}

// Function to read file as array buffer
function readFileAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

