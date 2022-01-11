
const savingBtn = document.getElementById("savingBtn");
const post = document.getElementById('post-box');

function open(){
  post.style.display="block";
  alert("click!");
}
savingBtn.addEventListener("onclick",open);
/*
function openClose() {
  if ($("#post-box").css("display") == "block") {
      $("#post-box").hide();
      $("#btn-post-box").text("포스팅 박스 열기");
  } else {
      $("#post-box").show();
      $("#btn-post-box").text("포스팅 박스 닫기");
  }
}
*/
function openClose() {
  if ($("#post-box").css("display") == "block") {
      $("#post-box").hide();
      $("#savingBtn").text("포스팅 박스 열기");
  } else {
      $("#post-box").show();
      $("#savingBtn").text("포스팅 박스 닫기");
  }
}
