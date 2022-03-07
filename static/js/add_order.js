function handle_change_images(files) {
  const imgs = document.getElementsByClassName("uploaded_images_div");
  const length = imgs.length;
  for (i = 0; i < length; i++) {
    const img = document.getElementsByClassName("uploaded_images_div")[0];
    img.parentNode.removeChild(img);
  }
  const windowURL = window.URL || window.webkitURL;
  for (j = 0; j < files.length; j++) {
    const dataURL = windowURL.createObjectURL(files[j]);
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
