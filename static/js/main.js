$('#add_designation').on('click', function(e) {
    let desi = document.getElementById("add_text").value;
    console.log(desi)
    let baseUrl = new URL(window.location.href);
    baseUrl = `${baseUrl.protocol}//${baseUrl.hostname}:${baseUrl.port}`;
    console.log(baseUrl);
    if (desi) {
        let val = desi.toLowerCase();
        axios({
            method: 'post',
            url: baseUrl + '/admin/add_designation',
            data: {
                designation: val
            }
        }).then(res => {
            data = res.data;
            console.log(data)
            if (data['success']) {
                alert(data['success']);
                $('.selectpicker').append($('<option>', {
                    value: data['designation_id'],
                    text: val
                })).selectpicker('val', val).selectpicker('refresh');
                location.reload(true);
            } else if(data['error']) {
                alert(data['error']);
            }

        }).catch(err =>{
            alert("ERROR");
            console.log(err);
        })
    }         
});

$('#add_project').on('click', function(e) {
    let proj = document.getElementById("add_text").value;
    // console.log(proj)
    let baseUrl = new URL(window.location.href);
    baseUrl = `${baseUrl.protocol}//${baseUrl.hostname}:${baseUrl.port}`;
    console.log(baseUrl);
    if (proj) {
        let val = proj.toLowerCase();
        axios({
            method: 'post',
            url: baseUrl + '/admin/add_project',
            data: {
                project: val
            }
        }).then(res => {
            data = res.data;
            if (data['msg']) {
                alert(data['msg']);
                $('.selectpicker').append($('<option>', {
                    value: val,
                    text: val
                })).selectpicker('val', val).selectpicker('refresh');
                location.reload(true);

            } 

        }).catch(err =>{
            alert("ERROR");
            console.log(err);
        })
    }         
});


$('#user-table #submit').on('click', function(e){
    e.preventDefault();
    let uReg = /^[A-Za-z][A-Za-z0-9_]{7,29}$/;
    let username = document.getElementById('new_user').value;

    if (!uReg.test(username)){
        alert("user name not valid");
    }

    let data = $('#add_user_form').serializeArray();
    let baseUrl = new URL(window.location.href);
    baseUrl = `${baseUrl.protocol}//${baseUrl.hostname}:${baseUrl.port}`;
    axios({
        method: 'POST',
        url: baseUrl + '/admin/add_user',
        data: data
    }).then(res => {

        res = JSON.parse(JSON.stringify(res));
        if (res['data']['msg']) {
            alert(res['data']['msg']);
        }
        // window.location.reload();
    }).catch(err =>{
        alert("ERROR");
        console.log(err);
    })
})

