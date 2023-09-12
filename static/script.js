const fromDate = document.getElementById("fromDate");
const toDate = document.getElementById("toDate");

fromDate.addEventListener("input",function(e){
    toDate.min = fromDate.value;
});

toDate.addEventListener("input",function(e){
    fromDate.max = toDate.value;
});


async function beforeExitEventHandler(e)
{
    e.preventDefault();
    const confirmationMessage = "Are you sure you want to leave this page?";
    e.returnValue = confirmationMessage;

    await callEmergencyExit()

    return confirmationMessage;
}

function formatDate(date){
    const day = date.getDate();
    const month = date.getMonth() + 1; 
    const year = date.getFullYear();

    return `${year}-${month}-${day}`;
}

function checkDates(dateFrom,dateTo){
    
    if(isNaN(dateFrom) || isNaN(dateTo))
    {
        isNaN(dateFrom) ? alert("Please Control the From Date") : alert("Please Control the To Date");
        return true;
    }
    return false;
}

const emailInput = document.getElementById("email");
const submitButton = document.getElementById("submit-button");
submitButton.addEventListener("click",async function(e) {
   e.preventDefault();
   const mail = emailInput.value;
   let measure = [];
   measure.push(comboBox.value);

   const dateFrom = new Date(fromDate.value);
   const dateTo = new Date(toDate.value);

   if(checkDates(dateFrom,dateTo)) 
       return;
  
   const formattedDateFrom = formatDate(dateFrom);
   const formattedDateTo = formatDate(dateTo);

    if(!isValidEmail(mail)) 
    {
        alert("Email Not Valid ");
        return;
    }
    submitButton.setAttribute("disabled","");
    prgrssBar.style.width = "3%";
    prgrssTxt.innerText = "Please wait " + "3%" + " Complete"

    await submitForm(mail,formattedDateFrom,formattedDateTo,measure);    
});
const prgrssBar = document.getElementById("prgrss-bar");
prgrssBar.style.width = "0%";
const prgrssTxt = document.getElementById("prgrss-txt");
prgrssTxt.innerText = "";

const toggleCheckbox = document.getElementById("toggleCheckbox");
const container1 = document.getElementById("container1");
const container2 = document.getElementById("container2");
const toggleSwitch = document.querySelector(".toggle-switch");
const comboBox = document.getElementById("comboBox");


/* 2nd Container Visual Elements */
const tagContainer = document.getElementById("tag-container");

let CHECK_ALL_ACTIVE = false;
const checkboxes = document.getElementById("mySelectOptions");

const prgrssBar2 = document.getElementById("prgrss-bar-2");
prgrssBar2.style.width = "0%";
const prgrssTxt2 = document.getElementById("prgrss-txt-2");
prgrssTxt2.innerText = "";


const checkAll = document.getElementById("checkAll");
checkAll.addEventListener("click",function(e){
    CHECK_ALL_ACTIVE = !CHECK_ALL_ACTIVE;
    let items = document.querySelectorAll('[name="dropdown-group"]');
    
    Array.prototype.map.call(items, (item)=> {
        item.checked = CHECK_ALL_ACTIVE;
    })
    checkBoxClick(e);
});

const mydropdown = document.getElementById("mydropdown");
mydropdown.addEventListener("click",function(e){
    const target = e.target;
    if(target.classList.contains("dropdown-label")){
        this.classList.toggle("on")
    }
})

const startButton = document.getElementById("start-button");
startButton.disabled = true;
startButton.addEventListener("click",async function(e) {
    e.preventDefault();

    const dateFrom = new Date(fromDate.value);
    const dateTo = new Date(toDate.value);
 
    if(checkDates(dateFrom,dateTo)) 
        return;
   
    const formattedDateFrom = formatDate(dateFrom);
    const formattedDateTo = formatDate(dateTo);


    const operation = "BACKUP_DOWNLOAD";

    let measurements = [];

    const checkedCheckboxes = checkboxes.querySelectorAll('input[type=checkbox]:checked');
    for (const item of checkedCheckboxes) {
        const checkboxValue = item.getAttribute('value');
        measurements.push(checkboxValue);
    }
    const data = {
        "email" : "",
        "measure": measurements,
        "operation": operation,
        "dateFrom": formattedDateFrom,
        "dateTo": formattedDateTo
    }
    const response = await callSubmitApi(data);
     if(response && response.status === 200) {
         startButton.disabled = true;
         checkOperationStatus(operation,prgrssBar2,prgrssTxt2,startButton);
       }
       else throw new Error("Requset Failed");
 });

const fileTable = document.getElementById("fileTable");
const downloadAllBtn = document.getElementById("downloadAll");
downloadAllBtn.setAttribute("hidden",'');
downloadAllBtn.addEventListener("click", function(e){
    e.preventDefault();
    let promise = callListFilestApi();
    promise.then((files)=> {
        files.forEach(file => {
            const link = document.createElement('a');
            link.href = `/api/download/${file}`;
            link.download = '';
            link.click();
        });
    }).catch(error => console.error('Error', error));
})


const tbody = fileTable.querySelector("tbody");
const cleanAll = document.getElementById("cleanAll");
cleanAll.setAttribute("hidden",'');
cleanAll.addEventListener("click", async function(e){
    e.preventDefault();
    const res = await callDeleteAllApi();
    if(res.status === 200)
    {
        alert("All CSV Files deleted");
        tbody.innerHTML = '';
        prgrssBar2.style.width = "0%";
        prgrssTxt2.innerText ="All CSV files Deleted";
        downloadAllBtn.setAttribute("hidden","");
        cleanAll.setAttribute("hidden","");
    }
})
 
window.onload = function () {
    //call api
    fetch("/api/measurements")
    .then(response => response.json())
    .then(measurements => {
        measurements.map(function(measure){
            addOption(comboBox, measure, measure);
            addCheckBox(checkboxes,measure,measure);
        });
    })
    .catch(error => console.error('Err' + error));
}


function isValidEmail(email) {
    // Regular expression to validate email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Check if the email is not empty and matches the pattern
    return email && emailPattern.test(email);
}


document.onclick = function(e) {
    const target = e.target;
    const flag = mydropdown.classList.contains("on")
    if(target.getAttribute("name") !== "dropdown-group" && flag && !target.classList.contains("dropdown-label")) {
        mydropdown.classList.remove("on");
    }
}

function checkBoxClick(e) {
    const items = document.querySelectorAll('[name="dropdown-group"]');
    Array.prototype.map.call(items, (item)=> {
        const found = checkIfChipExists(item.value);
        if(item.checked) {
            if(!found) {
                const timestamp = new Date().getTime();
                createChipElement(item.value,timestamp);
            }
        }
        else {
            if(found) {
                removeChip(item.value);
            }
        }
    })
}

function checkIfChipExists(txtContent){
    const tagElements = document.querySelectorAll("li.tag");
    const liArray = Array.from(tagElements);

    return liArray.some(li => {
        const aText = li.querySelector("a").textContent;
        
        if (aText === txtContent) {
           return true;
        }
    })   
}

function removeChip(txtContent){
    const tagElements = document.querySelectorAll("li.tag");

    tagElements.forEach(li => {
        const aText = li.querySelector("a").textContent;
        
        if (aText === txtContent) {
            li.remove();
        }
    });
}

function createChipElement(chipNameString,uuid) {
    const liElement = document.createElement('li');
   
    liElement.setAttribute("class","tag");
    liElement.setAttribute("id",uuid);
    const aElement = document.createElement("a");
    aElement.setAttribute("id",uuid);

    aElement.addEventListener("click",(e) => {
        self = e.target;
        uuid = self.getAttribute("id");

        const items = document.querySelectorAll('[name="dropdown-group"]');
        Array.prototype.map.call(items, (item)=> {
            if(item.checked && item.value === self.innerText) {
                  item.checked = false;
            }
        })
        const parent = document.getElementById(uuid);
        parent.remove();
    })

    aElement.innerText = chipNameString;
    liElement.appendChild(aElement);
    tagContainer.appendChild(liElement);
}

function addCheckBox(parent, value, text){
    const lblElement = document.createElement('label');
    lblElement.classList.add("dropdown-option");
    lblElement.innerText = text;
    const inputElement = document.createElement("input");
    inputElement.setAttribute('type','checkbox');
    inputElement.setAttribute('value',value);
    inputElement.setAttribute("name","dropdown-group");
    inputElement.addEventListener("click",checkBoxClick);
    lblElement.appendChild(inputElement);
    parent.appendChild(lblElement);
}

function addOption(selectElement, value, text){
    const newOption = document.createElement('option');
    newOption.value = value;
    newOption.textContent= text;
    selectElement.appendChild(newOption);
}

toggleCheckbox.addEventListener('change', function(){
    if (toggleCheckbox.checked) {
        // Activate the second FlexBox
        container2.classList.remove('inactive');
        container1.classList.add('inactive');
        toggleSwitch.classList.add('active');
        emailInput.setAttribute("disabled","");
        submitButton.setAttribute("disabled","");

        startButton.removeAttribute("disabled");
        prgrssBar2.removeAttribute("disabled");
        prgrssTxt2.removeAttribute("disabled");
        mydropdown.removeAttribute("disabled");
        

    } else {
        // Activate the first FlexBox
        container2.classList.add('inactive');
        container1.classList.remove('inactive');
        toggleSwitch.classList.remove('active');
        emailInput.removeAttribute("disabled")
        submitButton.removeAttribute("disabled")

        startButton.setAttribute("disabled","");
        prgrssBar2.setAttribute("disabled","");
        prgrssTxt2.setAttribute("disabled","");
        mydropdown.setAttribute("disabled","");
    }
});

function checkOperationStatus(operation,progressBar,progressText,yourButton){
    fetch("/api/files/current")
    .then(response => response.json())
    .then(result => {
        window.addEventListener("beforeunload", beforeExitEventHandler);

        if(result.status === "waiting"){
            progressBar.style.width = "3%";
            progressText.innerText = "Please wait " + "3%" + " Complete"
            setTimeout(checkOperationStatus,4000,operation,progressBar,progressText,yourButton);
        }
        else if (result.status === "finished"){
            yourButton.disabled = false;
            progressBar.style.width = "100%";
            progressText.innerText ="Operation Complete";
            window.removeEventListener("beforeunload", beforeExitEventHandler);

            if(operation === "BACKUP_DOWNLOAD"){
                // Call list files api
                const promise = callListFilestApi();
                promise.then((files)=> {
                    files.forEach((file)=> {
                        const row = document.createElement('tr');
                        const fileNameCell = document.createElement('td');
                        const actionCell = document.createElement('td');
                        const fileLink = document.createElement('a');

                        fileNameCell.textContent = file;
                        fileLink.textContent = 'Download';
                        fileLink.href = `/api/download/${file}`;
                        fileLink.setAttribute('download','');
                        actionCell.appendChild(fileLink);

                        row.appendChild(fileNameCell);
                        row.appendChild(actionCell);
                        tbody.appendChild(row);

                    })
                    downloadAllBtn.removeAttribute("hidden");
                    cleanAll.removeAttribute("hidden",'');
                })
                .catch(error => console.error('Error ', error));
            }
            else {
                submitButton.removeAttribute("disabled");
            } 
        }
        else {
            const fileNumber = result.fileNumber;
            const totalFiles = result.totalFiles;
            const fileName = result.fileName;

            let percent = (+fileNumber/+totalFiles)*100 +"";
            percent = percent.substring(0,4) + "%";
            progressBar.style.width = percent;

            progressText.innerText = fileName + " " + percent + " Complete"

            setTimeout(checkOperationStatus,4000,operation,progressBar,progressText,yourButton);
        }
    })
    .catch(error => {
        console.error("Error ",error);
        progressBar.style.width = "0%";
        progressText.innerText ="Operation Failed";
    })
}


async function submitForm(email,dateFrom,dateTo,measure) {
    
    const operation = "BACKUP_COMPRESS_EMAIL";

    // create an object to send json data
    const data = {
        "email" : email,
        "measure": measure,
        "operation": operation,
        "dateFrom": dateFrom,
        "dateTo": dateTo
    }

    const response = await callSubmitApi(data);    
    if(response.status === 200) {
        submitButton.disabled = true;
        checkOperationStatus(operation,prgrssBar,prgrssTxt,submitButton);
    }
    else throw new Error("Requset Failed");
}


async function callSubmitApi(data) {
    return fetch("/api/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
        body: JSON.stringify(data)
    }).then( response => {
        return response;
    })
    .catch(error => {
        console.error("Error ",error);
    })
}

async function callListFilestApi() {
    return fetch("/api/list_files").then( response => {
        return response.json();
    })
    .catch(error => {
        console.error("Error ",error);
    })
}

async function callDeleteAllApi() {
    return fetch("/api/deleteAll").then( response => {
        return response;
    })
    .catch(error => {
        console.error("Error ",error);
    })
}

async function callEmergencyExit(){
        return fetch("/api/doexit").then( response => {
            return response.json();
        })
        .catch(error => {
            console.error("Error ",error);
        })
}