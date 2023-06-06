var input = document.getElementById('avatar');
console.log("*************************************",input)
if(input) {
  input.addEventListener('change', function () {
    getUploadImageUrl(this);
  });
  console.log("----------------", input)
}

function getUploadImageUrl(input) {
  console.log("----------------", input.files)

  if (input.files && input.files[0]) {
    var reader = new FileReader();
    console.log("----------------", reader)

    reader.onload = function (e) {
      document.getElementById('avatar_preview').setAttribute('src', e.target.result);
      console.log("----------------", e)
    };

    reader.readAsDataURL(input.files[0]);
  }
}