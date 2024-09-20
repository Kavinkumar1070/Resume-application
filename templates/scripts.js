// Redirect to Resume Checker page
document.getElementById('resumeCheckerBtn')?.addEventListener('click', function() {
  window.location.href = '/templates/check_resume.html';
});

// Redirect to Job Description page
document.getElementById('jobDescBtn')?.addEventListener('click', function() {
  window.location.href = '/templates/resumejd.html';
});

// Handle file upload and preview for Resume Checker
document.getElementById('resumeUpload')?.addEventListener('change', function(event) {
  handleFileUpload(event, 'resumePreview');
});

// Handle file upload and preview for Job Description page
document.getElementById('jobResumeUpload')?.addEventListener('change', function(event) {
  handleFileUpload(event, 'jobResumePreview');
});

// Scan button functionality for Resume Checker
document.getElementById('scanResumeBtn')?.addEventListener('click', function() {
  showLoader('/templates/results.html'); // Pass the results page URL
});

// Scan button functionality for Job Description
document.getElementById('scanJobDescBtn')?.addEventListener('click', function() {
  showLoader('/templates/results.html'); // Pass the results page URL
});

// Function to handle file upload and preview
function handleFileUpload(event, previewId) {
  const file = event.target.files[0];
  const previewContainer = document.getElementById(previewId);
  previewContainer.innerHTML = ''; // Clear previous content

  if (file) {
    const fileType = file.type;

    if (fileType.includes('image')) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'contain';
        previewContainer.appendChild(img);
      };
      reader.readAsDataURL(file);
    } else if (fileType === 'application/pdf') {
      const reader = new FileReader();
      reader.onload = function(e) {
        const iframe = document.createElement('iframe');
        iframe.src = e.target.result;
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        previewContainer.appendChild(iframe);
      };
      reader.readAsDataURL(file);
    } else {
      const unsupportedMessage = document.createElement('div');
      unsupportedMessage.innerHTML = `<p>Unsupported file type: ${file.name}</p>`;
      unsupportedMessage.style.display = 'flex';
      unsupportedMessage.style.alignItems = 'center';
      unsupportedMessage.style.justifyContent = 'center';
      unsupportedMessage.style.height = '100%';
      previewContainer.appendChild(unsupportedMessage);
    }
  }
}

// Exit button functionality
document.getElementById('exitBtn')?.addEventListener('click', function() {
  window.location.href = '/templates/front_page.html';
});

// Show loader function
function showLoader(redirectUrl) {
  const loadingScreen = document.getElementById('loadingScreen');
  loadingScreen.classList.remove('hidden');
  loadingScreen.style.visibility = 'visible'; // Make it visible

  const loadingMessages = [
      'Processing...',
      'Analyzing...',
      'Almost done...'
  ];
  
  let i = 0;

  const interval = setInterval(() => {
      const loadingTextElement = document.getElementById('loadingText');
      const tickElement = document.getElementById('tick');
      
      const messageWithTick = `✔️ ${loadingMessages[i]}`;
      loadingTextElement.innerText = messageWithTick;
      
      tickElement.classList.add('visible'); // Make tick visible
      setTimeout(() => tickElement.classList.remove('visible'), 800); // Hide after 800ms

      i++;

      if (i === loadingMessages.length) {
          clearInterval(interval);
          // Delay before redirecting
          setTimeout(() => {
              window.location.href = redirectUrl;
          }, 1500);
      }
  }, 1500);
}
