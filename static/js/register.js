// several check function
function check_username() {
  const len = $("#username").val().length;
  if ((len > 0 && len < 5) || len > 20) {
    $("#username").next().html("Username should between 5-20 characters!");
    $("#username").next().show();
  } else {
    $("#username").next().hide();
  }
}
function check_password() {
  const len = $("#password").val().length;
  if ((len > 0 && len < 6) || len > 20) {
    $("#password").next().html("Password should between 6-20 characters!");
    $("#password").next().show();
  } else {
    $("#password").next().hide();
  }
}
function check_confirm_password() {
  if ($("#password").val() != $("#confirm_password").val()) {
    console;
    $("#confirm_password")
      .next()
      .html(
        "Password doesn't match. Please check that you've entered the same password twice"
      );
    $("#confirm_password").next().show();
  } else {
    $("#confirm_password").next().hide();
  }
}
function check_submit() {
  // simple if code, not use regular expression because the condition is simple, and let code easy to understand.
  if (
    $("#password").val() == $("#confirm_password").val() &&
    $("#username").val().length >= 5 &&
    $("#username").val().length <= 20 &&
    $("#password").val().length >= 6 &&
    $("#password").val().length <= 20
  ) {
    var form = document.getElementById("register-form");
    form.submit();
  } else {
    alert("Error! Please check the input.");
    return false;
  }
}