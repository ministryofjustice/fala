const cookieBanner = document.getElementById("cookie-banner");
const defaultMessage = document.getElementById("default-message");
const acceptedMessage = document.getElementById("accepted-message");
const rejectedMessage = document.getElementById("rejected-message");

// Set cookies
const setCookie = (name, value, days) => {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = ";expires=" + date.toUTCString();
  }
  document.cookie = `${name}=${value}${expires};path=/;samesite=lax`;
}

// Accept analytics cookies
const acceptCookieBanner = document.getElementById("accept-cookies");
if (acceptCookieBanner) {
  acceptCookieBanner.addEventListener("click", () => {
    setCookie("cookiePermission", "Allowed", 30);
    defaultMessage.hidden = true;
    acceptedMessage.hidden = false;
  })
};

// Reject analytics cookies
const rejectCookieBanner = document.getElementById("reject-cookies");
if (rejectCookieBanner) {
  rejectCookieBanner.addEventListener("click", () => {
    setCookie("cookiePermission", "Rejected", 30);
    defaultMessage.hidden = true;
    rejectedMessage.hidden = false;
  })
};

// Hide accepted message
const hideCookieAcceptMessage = document.getElementById("accepted-hide");
if (hideCookieAcceptMessage) {
  hideCookieAcceptMessage.addEventListener("click", () => {
    acceptedMessage.hidden = true;
    cookieBanner.hidden = true;
  })
};

// Hide rejected message
const hideCookieRejectMessage = document.getElementById("rejected-hide");
if (hideCookieRejectMessage) {
  hideCookieRejectMessage.addEventListener("click", () => {
    rejectedMessage.hidden = true;
    cookieBanner.hidden = true;
  })
};

// Cookie policy form
const cookiePolicyForm = document.getElementById("cookie_policy_page_choice");
if (cookiePolicyForm) {
  cookiePolicyForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const selectedValue = document.querySelector("input[name='cookies']:checked").value;
    const notificationBanner = document.getElementById('cookieChoiceNotificationBanner');
    if (selectedValue === "Allowed") {
      setCookie("cookiePermission", "Allowed", 30);
      tagMan();
      if (cookieBanner) {
        cookieBanner.hidden = true;
      }
      if (notificationBanner) {
        notificationBanner.classList.remove("hidden");
        notificationBanner.scrollIntoView()
      }
    } else if (selectedValue === "Rejected") {
      setCookie("cookiePermission", "Rejected", 30);
      if (cookieBanner) {
        cookieBanner.hidden = true;
      }
      if (notificationBanner) {
        notificationBanner.classList.remove("hidden");
        notificationBanner.scrollIntoView()
      }
    }
  });
};
