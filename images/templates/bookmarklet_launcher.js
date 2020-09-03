(function(){
    if (window.myBookmarklet != undefined){ //here check whether the bookmarklet has been already loaded by checking whether the mybookmarklet variable is defined,by doing so,we avoid loading it again if the user clicks on the bookmarklet repeatedly
        myBookmarklet();
    }
    else { // if mybookmarklet is not defined we load another javascript file by adding a <script> element to the document,the script tag loads the bookmarklet.js script using a random number as a parameter to prevent loading the file from the browser's cache
      document.body.appendChild(document.createElement('script')).src='https://452e0f310259.ngrok.io/static/js/bookmarklet.js?
      r='+Math.floor(Math.random()*99999999999999999999);

    }
})();
