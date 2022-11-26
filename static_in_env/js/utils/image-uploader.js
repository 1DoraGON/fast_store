const elementHtml = `<div class="container_i">
<div class="wrapper">
   <div class="image">
        <img class="primary-image custom-btn" src="" onclick="defaultBtnActive()" alt="">
   </div>
   <div class="content">
      <div class="icon">
         <i class="fas fa-cloud-upload-alt"></i>
      </div>
      <div class="text">
         No file chosen, yet!
      </div>
   </div>
   <div class="cancel-btn">
      <i class="fas fa-times"></i>
   </div>
   <div class="file-name">
      File name here
   </div>
</div>
<input name="image" class="default-btn" type="file" accept=".jpg , .jpeg ,.png" hidden>
</div>`

var wrapper 
var fileName
var defaultBtn
var customBtn
var cancelBtn
var img
var id = 0
var myId
const imagesSection = document.querySelector("#images");
const defaultImage = document.querySelector(`.container_image_0 .custom-btn`).getAttribute("src")

const elementsSelector = (id) => {
   wrapper = document.querySelector(`.container_image_${id} .wrapper`);
   fileName = document.querySelector(`.container_image_${id} .file-name`);
   defaultBtn = document.querySelector(`.container_image_${id} .default-btn`);
   customBtn = document.querySelector(`.container_image_${id} .custom-btn`);
   cancelBtn = document.querySelector(`.container_image_${id} .cancel-btn i`);
   img = document.querySelector(`.container_image_${id} .custom-btn`);
   input = document.querySelector(`.container_image_${id} input`);
   img.src= defaultImage
   input.myId = id
   input.addEventListener("change", function(e){
      myId = e.target.myId
      const file = this.files[0];
      if(file){
        const reader = new FileReader();
        reader.onload = function(){
         const result = reader.result;
         wrapper.classList.add("active");
         img.disabled = true
         img.removeAttribute("onclick");
         id++
         img.src = result;
         createElement(id)
         
      }
       cancelBtn.addEventListener("click", function(){
         const container = document.querySelector(`.container_image_${id-1}`);
         container.remove()
         })
         reader.readAsDataURL(file);
      }
      if(this.value){
         let valueStore = this.value.match(regExp);
         fileName.textContent = valueStore;
      }
   });
}
const createElement = (id) => {
   const newElement = document.createElement('div')
   newElement.classList.add("col-sm")
   newElement.classList.add(`container_image_${id}`)
   newElement.innerHTML = elementHtml
   imagesSection.appendChild(newElement)
   elementsSelector(id)
}
elementsSelector(id)
let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;
function defaultBtnActive(){
  input.click();
}

