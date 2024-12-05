function init_file() {
var user_name = document.getElementById('loginEmail').value;
var pass_word = document.getElementById('loginPassword').value;
if (user_name.trim() === '')
     {
       document.getElementById("lb_login_username").className = '';
       document.getElementById('lb_login_username').innerHTML = 'Username is required!';
       return false;
    }
    else
    {
       document.getElementById("lb_login_username").className = 'error_r';
       document.getElementById('lb_login_username').innerHTML = '';
    }
    if (pass_word.trim() === '')
     {
       document.getElementById("lb_login_password").className = '';
       document.getElementById('lb_login_password').innerHTML = 'Password is required!';
       return false;
    }
    else
    {
       document.getElementById("lb_login_password").className = 'error_r';
       document.getElementById('lb_login_password').innerHTML = '';
    }

document.getElementById("multiform").action = '/login';
document.getElementById("multiform").submit();
return true;
}

function init_register()
{
    var reg_username = document.getElementById('registerName');
    var reg_email = document.getElementById('registerEmail');
    var reg_password = document.getElementById('registerPassword');
    var confi_reg_password = document.getElementById('rconfirmPassword');
    const checkbox = document.getElementById("checkbox");
    const isChecked = checkbox.checked;
    var mfa_enabled=''

    document.getElementById("lb_Username").className = 'error_r';
    document.getElementById("lb_email").className = 'error_r';
    document.getElementById("lb_password").className = 'error_r';
    document.getElementById("lb_conf_password").className = 'error_r';

    const usernameValue = reg_username.value.trim();
    const emailValue = reg_email.value.trim();
    const passwordValue = reg_password.value.trim();
    const password2Value = confi_reg_password.value.trim();

    if (usernameValue === '')
     {
       document.getElementById("lb_Username").className = '';
       document.getElementById('lb_Username').innerHTML = 'Name is required!';
       return false;
    }
    else
    {
       document.getElementById("lb_Username").className = 'error_r';
       document.getElementById('lb_Username').innerHTML = '';
    }
    if (emailValue === '') {
     document.getElementById("lb_email").className = '';
     document.getElementById('lb_email').innerHTML = 'Email is required!';
     return false;
    }
    else if (!isValidEmail(emailValue)) {
        document.getElementById("lb_email").className = '';
        document.getElementById('lb_email').innerHTML = 'Provide a valid email address!';
        return false;
    }
    else {
        document.getElementById("lb_email").className = 'error_r';
        document.getElementById('lb_email').innerHTML = '';
    }

    if (passwordValue === '') {
        document.getElementById("lb_password").className = '';
        document.getElementById('lb_password').innerHTML = 'Password is required!';
        return false;
    } else if (passwordValue.length < 8) {
        document.getElementById("lb_password").className = '';
        document.getElementById('lb_password').innerHTML = 'Password must be at least 8 character.';
        return false;
    }
    else {
        document.getElementById("lb_password").className = 'error_r';
        document.getElementById('lb_password').innerHTML = '';
    }
    if (password2Value === '') {
        document.getElementById("lb_conf_password").className = '';
        document.getElementById('lb_conf_password').innerHTML = 'Please confirm your password.';
        return false;
    }
    else if (password2Value !== passwordValue) {
        document.getElementById("lb_conf_password").className = '';
        document.getElementById('lb_conf_password').innerHTML = "Passwords doesn't match";
        return false;
    }
    else {
       document.getElementById("lb_conf_password").className = 'error_r';
        document.getElementById('lb_conf_password').innerHTML = '';
    }

    var check_list={'reg_username':reg_username.value,"reg_email":reg_email.value}
    $.ajax({
                url: '/check_for_gmail',
                data: JSON.stringify(check_list),
                type: 'POST',
                contentType: "application/json",
                dataType: 'json',
                success: function (data)
                {
                    console.log(data['msg']);
                      if(data["msg"]=='email_id'){
                          document.getElementById("lb_email").className = '';
                         document.getElementById('lb_email').innerHTML = 'Email is already taken!';
                         return false
                      }
                      else{
                          document.getElementById("lb_email").className = 'error_r';
                         document.getElementById('lb_email').innerHTML = '';
                      }
                          if (isChecked)
                          {
                           mfa_enabled='yes';
                          }
                          else
                          {
                          mfa_enabled='no';
                          }
                    var g_recaptcha_response = document.getElementById('g-recaptcha-response');
                    const g_recaptcha_response_ = g_recaptcha_response.value
                    var final_bills_request={"reg_username":reg_username.value,"reg_email":reg_email.value,"reg_password":reg_password.value,"mfa_enabled":mfa_enabled,"g_recaptcha_response":g_recaptcha_response_};
                    $.ajax({
                                url: '/register',
                                data: JSON.stringify(final_bills_request),
                                type: 'POST',
                                contentType: "application/json",
                                dataType: 'json',
                                success: function (data1)
                                {

                                    if(data1['status']=="Registration successful!" && (data1['qr_code_data']=='yes'))
                                    {
                                        window.location.href = "/enable_2fa/"+data1['header_id']
                                    }
                                    else if ( data1['qr_code_data']=='no')
                                    {
                                       alert(data1['status'])
                                       window.location.href = "/login"
                                    }
                                    else{
                                        alert(data1['status'])
                                        return false;
                                    }

                                },
                                error: function(data1)
                                {
                                    console.log(data1);
                                    return false;
                                }
                        });

                },
                error: function(data)
                {
                    console.log(data);
                    return false;
                }
        });

}




function Submit_function(){
    var header_id = document.getElementById("header_id").value;
    const otpInputs = document.querySelectorAll('.otp-input');

    // Collect the values of each input
    let otpValue = '';
    otpInputs.forEach(input => {
        otpValue += input.value;
    });
    var details_={"token":otpValue,"header_id":header_id}
    $.ajax({
            url: '/enable_2fa_final',
            data: JSON.stringify(details_),
            type: 'POST',
            contentType: "application/json",
            dataType: 'json',
            success: function (data2)
            {
              if(data2['status']=="successful!")
            {
                window.location.href = "/home"
            }
            else{
                alert(data2['status'])
                return false;
            }
            },
            error: function(data2)
            {
              document.getElementById("order_fuel_id").disabled = true;
              document.getElementById("Get_Quote_id").disabled = true;
                console.log(data2);
            }
    });
}



function payment_submission(){
    var price_selected = document.getElementById("price_selected").value;
    var type_of_subscription = document.getElementById("type_of_subscription").value;
    var cardNumber = document.getElementById("cardNumber").value;
    var cardName = document.getElementById("cardName").value;
    var cardMonth = document.getElementById("cardMonth").value;
    var cardYear = document.getElementById("cardYear").value;
    var cardCvv = document.getElementById("cardCvv").value;

    if (cardNumber.trim() === '')
     {
       document.getElementById("erroe_in_card").className = '';
       document.getElementById('erroe_in_card').innerHTML = 'Card Number Is Required!';
       return false;
    }
    else if (cardName.trim() === '')
     {
       document.getElementById("erroe_in_card").className = '';
       document.getElementById('erroe_in_card').innerHTML = 'Card Holder Name Is Required!';
       return false;
    }
    else if (cardMonth === '')
     {
       document.getElementById("erroe_in_card").className = '';
       document.getElementById('erroe_in_card').innerHTML = 'Please Select Month!';
       return false;
    }
    else if (cardYear === '')
     {
       document.getElementById("erroe_in_card").className = '';
       document.getElementById('erroe_in_card').innerHTML = 'Please Select Year!';
       return false;
    }
    else if (cardCvv.trim() === '')
     {
       document.getElementById("erroe_in_card").className = '';
       document.getElementById('erroe_in_card').innerHTML = 'CVV Is Required!';
       return false;
    }
    else
    {
       document.getElementById("erroe_in_card").className = 'error_r';
       document.getElementById('erroe_in_card').innerHTML = '';
    }

    var details_={"price_selected":price_selected,"type_of_subscription":type_of_subscription,"cardNumber":cardNumber,"cardName":cardName,"cardMonth":cardMonth,"cardYear":cardYear,"cardCvv":cardCvv}
    $.ajax({
            url: '/sub',
            data: JSON.stringify(details_),
            type: 'POST',
            contentType: "application/json",
            dataType: 'json',
            success: function (data2)
            {
              if(data2['status']=="success")
            {
                window.location.href = "/home"
            }
            else{
                alert("Error while pushing data, Please try again some time")
                return false;
            }
            },
            error: function(data2)
            {
              alert("Error while pushing data, Please try again some time")
              return false;
            }
    });

}


//const password2 = document.getElementById('password2');

const isValidEmail = email => {
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(String(email).toLowerCase());
        }



function insert_into_database(moduleId){
    var courses_status_id = document.getElementById("courses_status_id").value;
    var courses_id = document.getElementById("courses_id").value;

    var details_={"moduleId":moduleId,"courses_status_id":courses_status_id}
    $.ajax({
            url: '/load_course/sql/'+courses_id,
            data: JSON.stringify(details_),
            type: 'POST',
            contentType: "application/json",
            dataType: 'json',
            success: function (data2)
            {
              if(data2['status']=="Success")
            {
                 alert(moduleId + ' is complete!');
                 return true;
            }
            else if(data2['status']=="existed")
            {
                 alert("Model is already Completed");
                 return true;
            }
            else{
                alert(data2['message'])
                window.location.href = "/login"
            }
            },
            error: function(data2)
            {
              alert(moduleId + ' not complete, Please refresh the page and try again!');
              window.location.href = "/login"
            }
    });
}