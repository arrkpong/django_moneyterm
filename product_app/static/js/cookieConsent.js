// product_app\static\js\cookieConsent.js
document.addEventListener('DOMContentLoaded', function () {
  // ฟังก์ชันสำหรับตั้งค่าคุกกี้
  function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + d.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
  }

  // ฟังก์ชันสำหรับรับคุกกี้
  function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  // แสดงโมดัลหากยังไม่ได้ตั้งค่าความยินยอมต่อคุกกี้
  const cookieConsent = getCookie("cookie_consent");
  if (!cookieConsent) {
    const cookieConsentModal = new bootstrap.Modal(document.getElementById('cookieConsentModal'), {});
    cookieConsentModal.show();
  }

  // ตั้งค่าความยินยอมต่อคุกกี้เมื่อผู้ใช้ตกลง
  document.getElementById('acceptCookies').addEventListener('click', function () {
    setCookie("cookie_consent", "accepted", 365);
    const cookieConsentModal = bootstrap.Modal.getInstance(document.getElementById('cookieConsentModal'));
    cookieConsentModal.hide();
  });

  // ปฏิเสธคุกกี้เมื่อผู้ใช้คลิกที่ลิงก์
  document.getElementById('rejectCookies').addEventListener('click', function () {
    setCookie("cookie_consent", "rejected", 365);
    const cookieConsentModal = bootstrap.Modal.getInstance(document.getElementById('cookieConsentModal'));
    cookieConsentModal.hide();
  });
});
