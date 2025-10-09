const fala_form = document.querySelector('#fala_questions');
const fala_postcode_only_form = document.querySelector('#fala_questions_for_tailored_results');

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const cookie_value = getCookie('cookiePermission') === 'Allowed';

if (fala_form && cookie_value) {
    fala_form.addEventListener('submit', function(e){

    // variables for postcode and organisation name
    const postcode = document.querySelector("#id_postcode").value;
    const organisation = document.querySelector("#id_name").value;

    // variables for checkbox
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const selected = Array.from(checkboxes).map(x => x.value);

    window.dataLayer.push({
      'event': "formSubmission",
      'postcode': postcode,
      'organisation': organisation,
      'checkbox': selected,
    });
  });
};

if (fala_postcode_only_form && cookie_value) {
  fala_postcode_only_form.addEventListener('submit', function(e){

  // variables for postcode
  const postcode = document.querySelector("#id_postcode").value;

  window.dataLayer.push({
    'event': "formSubmissionForTailoredResults",
    'postcode': postcode,
  });
});
};
