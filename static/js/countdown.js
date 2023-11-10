function formatTime(seconds) {
  let minutes = Math.floor(seconds / 60);
  let remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, "0")}:${remainingSeconds.toString().padStart(2, "0")}`;
}

function startCountdown(seconds, redirectUrl) {
  let countdownElement = document.getElementById("countdown");
  countdownElement.innerHTML = formatTime(seconds);

  let interval = setInterval(function () {
    seconds--;
    countdownElement.innerHTML = formatTime(seconds);

    if (seconds <= 0) {
      clearInterval(interval);
      window.location.href = redirectUrl;
    }
  }, 1000);
}

document.addEventListener("DOMContentLoaded", function () {
  let remainingTime = parseInt(document.getElementById('remainingTime').textContent);
  let redirectUrl = document.getElementById('redirectUrl').textContent;
  startCountdown(remainingTime, redirectUrl);
});
