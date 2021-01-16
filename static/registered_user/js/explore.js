
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
      }
    function reload_auto() {
        btn = document.querySelector('#btn-interest')
        btn.innerHTML = "remove";
        console.log('hello')
        return false
        
    }
    //   function interest() {

    //     // let btn = document.querySelector('#btn-interest');
    //     // console.log('hey there')
    //     // let btn_name = document.querySelector('#btn-interest').name;
    //     // btn.innerHTML = "Remove";
    //     // btn_value = "remove";
    //     location.reload()
    //     return false;
    // }

    // function notinterest() {
    //     // let btn = document.querySelector('#btn-remove');
    //     // console.log('hey there2')
    //     // let btn_name = document.querySelector('#btn-remove').name;
    //     // btn.innerHTML = "Interested?";
    //     // btn_value = "interest";
    //     location.reload()
    //     return false;
    // }

    // $(function() {
    //   $('.filterform_main').submit(function(event) {
    //       event.preventDefault();
    //       $(this).submit();
    //       }); 
    //   });
  
// function getValuesFromForm() {

//   // printValues(minagevalue = minage,maxagevalue = maxage, salaryvalue = salary,castevalue = caste,religionvalue = religion, gendervalue = gender, statevalue = state)
// }

// function printValues(minagevalue,maxagevalue,salaryvalue,castevalue,religionvlue,gendervalue,statevalue){
 
// }

function filtersubmit() {
  var genderarray = []
  var filter = document.getElementById('filterbtn');
  var minage = document.getElementById('minage');
  var maxage = document.getElementById('maxage');
  var salary = document.getElementById('salary');
  var caste = document.getElementById('caste');
  var religion = document.getElementById('religion');
  var genderchoise = document.querySelectorAll('.gendercheckbox');
  var state = document.getElementById('state');
  var testdiv = document.getElementById('testdiv');
  sessionStorage.setItem('state',JSON.stringify(state.value))
  sessionStorage.setItem('caste',JSON.stringify(caste.value))
  sessionStorage.setItem('religion',JSON.stringify(religion.value))
  sessionStorage.setItem('minage',JSON.stringify(minage.value))
  sessionStorage.setItem('maxage',JSON.stringify(maxage.value))
  sessionStorage.setItem('salary',JSON.stringify(salary.value))

  genderchoise.forEach(function(gender){

    genderarray.push({id: gender.id,checked: gender.checked});
  
  });
  // sessionStorage.setItem('gender',gender.value)
  sessionStorage.setItem('gender',JSON.stringify(genderarray));  

}

function loaddata(){
  var minage = document.getElementById('minage');
  document.getElementById('minage').value = JSON.parse(sessionStorage.getItem('minage'));
  document.getElementById('maxage').value = JSON.parse(sessionStorage.getItem('maxage'));
  document.getElementById('salary').value = JSON.parse(sessionStorage.getItem('salary'));
  document.getElementById('caste').value = JSON.parse(sessionStorage.getItem('caste'));
  document.getElementById('religion').value = JSON.parse(sessionStorage.getItem('religion'));
  document.getElementById('state').value = JSON.parse(sessionStorage.getItem('state'));
  var genderchoise = JSON.parse(sessionStorage.getItem('gender'))
  genderchoise.forEach(function(gender){
  document.getElementById(gender.id).checked = gender.checked;

  });
  // console.log('gender:',genderchoise)
}
// loaddata();
function clearSessionStorageData(){
  sessionStorage.clear();
}
// console.log(genderarray)
