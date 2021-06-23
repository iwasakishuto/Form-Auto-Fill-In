// Add Pop-Up Window for GraphViz Images.
function addPopUpViewer(element){
  const images = document.querySelectorAll(element);

  for(let i=0; i<images.length; i++){
    images[i].addEventListener("click", openPopUpGraphViz)
  }

  function openPopUpGraphViz(){
    const filter = document.createElement('div');
    filter.setAttribute("id", "pixel-viewer");

    const div_img = document.createElement('img');
    div_img.setAttribute("id",  "pixel-viewer__img");
    div_img.setAttribute("src", this.src);

    document.body.appendChild(filter);
    filter.appendChild(div_img);

    filter.addEventListener('click', close, {once: true});
    function close(){
      filter.className = 'fadeout';
      filter.addEventListener("animationend",function(){
        filter.remove();
      });
    }
  }
}

document.addEventListener('DOMContentLoaded', function(){
  addPopUpViewer(element="article img");
}, false);