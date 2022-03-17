// search function
function handle_search() {
  const page_url = window.location.href;
  const value = $("#search").val().replace(" ", "");
  if (value !== "") {
    if (page_url.indexOf("?") !== -1) {
      part_page_url = page_url.substring(0, page_url.indexOf("?"));
      // jump to page 1 because result may not have enough page
      const new_url =
        part_page_url + "?keywords=" + value;
      window.location.href = new_url;
      $("#search").val = value;
    } else {
      const new_url =
        page_url + "?keywords=" + value;
      window.location.href = new_url;
      $("#search").val = value;
    }
  }
}

// page select function
function jump_to(param) {
  // page_num, but get by Element, because can not get param from page
  const page_num =
    param == -2
      ? 1
      : param == -1
      ? Number($("#page_num").text()) - 1
      : param == 1
      ? Number($("#page_num").text()) + 1
      : Number($("#total_num").text());
  const page_url = window.location.href;
  if (page_url.indexOf("?") !== -1) {
    let i = page_url.indexOf("page=");
    let new_url;
    if (i !== -1){
      new_url = page_url.substring(0, i) + "page=" + page_num + "&size=10";
    } else {
      new_url = page_url + "&page=" + page_num + "&size=10";
    }
    window.location.href = new_url;
  } else {
    const new_url = page_url + "?page=" + page_num + "&size=10";
    window.location.href = new_url;
  }
}
