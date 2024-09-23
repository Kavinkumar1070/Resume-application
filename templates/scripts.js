// Redirect to Resume Checker page
document.getElementById('resumeCheckerBtn')?.addEventListener('click', function() {
  window.location.href = '/templates/check_resume.html';
});

// Redirect to Job Description page
document.getElementById('jobDescBtn')?.addEventListener('click', function() {
  window.location.href = '/templates/resumejd.html';
});



// Handle file upload and preview for Job Description page
document.getElementById('jobResumeUpload')?.addEventListener('change', function(event) {
  handleFileUpload(event, 'jobResumePreview');
});

// Scan button functionality for Resume Checker

// Scan button functionality for Job Description
document.getElementById('scanJobDescBtn')?.addEventListener('click', function() {
  showLoader('/templates/results.html'); // Pass the results page URL
});

// Function to handle file upload and preview


// Exit button functionality
document.getElementById('exitBtn')?.addEventListener('click', function() {
  window.location.href = '/templates/front_page.html';
});

