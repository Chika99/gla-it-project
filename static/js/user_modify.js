// function to insert image element to enable image pre-view in page
function handle_change_avatar(files) {
    const imgs = document.getElementsByClassName("uploaded_images_div");
    const length = imgs.length;
    if(length == 1){
      const img = document.getElementsByClassName("uploaded_images_div")[0];
      img.parentNode.removeChild(img);
    }
    if(files.length==1){
      const windowURL = window.URL || window.webkitURL;
      const dataURL = windowURL.createObjectURL(files[0]);
      const div = document.createElement("div");
      div.className = "uploaded_images_div";
      const image = document.createElement("img");
      image.src = dataURL;
      image.className = "uploaded_images";
      div.appendChild(image);
      document
        .getElementById("images_out")
        .insertBefore(div, document.getElementById("input_label"));
    }
  }