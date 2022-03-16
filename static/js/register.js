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
// $(function () {
//   var error_name = false;
//   var error_password = false;
//   var error_check_password = false;
//   var error_email = false;
//   var error_check = false;

//   $("#user_name").blur(function () {
//     check_user_name();
//   });

//   $("#pwd").blur(function () {
//     check_pwd();
//   });

//   $("#cpwd").blur(function () {
//     check_cpwd();
//   });

//   $("#email").blur(function () {
//     check_email();
//   });

//   function check_user_name() {
//     var len = $("#user_name").val().length;
//     if (len < 5 || len > 20) {
//       $("#user_name")
//         .next()
//         .html("Please enter a username between 5-20 characters!");
//       $("#user_name").next().show();
//       error_name = true;
//     } else {
//       $("#user_name").next().hide();
//       error_name = false;
//     }
//   }

//   function check_pwd() {
//     var len = $("#pwd").val().length;
//     if (len < 6 || len > 20) {
//       $("#pwd").next().html("Please enter a password between 6-20 characters!");
//       $("#pwd").next().show();
//       error_password = true;
//     } else {
//       $("#pwd").next().hide();
//       error_password = false;
//     }
//   }

//   function check_cpwd() {
//     var pass = $("#pwd").val();
//     var cpass = $("#cpwd").val();

//     if (pass != cpass) {
//       $("#cpwd").next().html("The two entered passwords do not match!");
//       $("#cpwd").next().show();
//       error_check_password = true;
//     } else {
//       $("#cpwd").next().hide();
//       error_check_password = false;
//     }
//   }

//   function check_email() {
//     var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

//     if (re.test($("#email").val())) {
//       $("#email").next().hide();
//       error_email = false;
//     } else {
//       $("#email").next().html("The email is not correct!");
//       $("#email").next().show();
//       error_check_password = true;
//     }
//   }

//   $("#reg_form").submit(function () {
//     check_user_name();
//     check_pwd();
//     check_cpwd();
//     check_email();

//     if (
//       error_name == false &&
//       error_password == false &&
//       error_check_password == false &&
//       error_email == false &&
//       error_check == false
//     ) {
//       return true;
//     } else {
//       return false;
//     }
//   });
// });
