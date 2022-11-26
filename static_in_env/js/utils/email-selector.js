
const emailElement = $('#id_email')
let selector = $('#email-selector')
$(emailElement).on('focus',()=>{
    selector.css("display", "block")
    //console.log(selector);
})
/* $(emailElement).on('focusout',()=>{
    selector.css("display","none")
    //console.log(selector);
}) */
$(emailElement).on('keyup',(e)=>{
    getEmail(e.target.value)
})

const getEmail = (email)=>{
    $.ajax({
        url: '/supervisor/get-email',
        type: 'get',
        data:{
            'email': email
        },
        dataType: 'json',
        success: function(response){
            console.log(response);
            showEmails(response['emails'])
        }
     });
}
const showEmails = (emails)=>{
    selector.empty()
    emails.forEach(email => {
        let emailItem = $('<button>')
        emailItem.addClass("list-group-item")
        emailItem.addClass("list-group-item-action")
        emailItem.attr("type","button")
        emailItem.html(email)
        $(emailItem).on('click',(e)=>{
            emailElement.val(e.target.innerHTML)
            console.log(emailElement);
        })
        selector.append(emailItem)
    });
}