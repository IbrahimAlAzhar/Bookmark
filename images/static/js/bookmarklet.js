(function(){
    var jquery_version = '3.3.1'; // the jquery version to load
    var site_url = 'https://452e0f310259.ngrok.io/'; // base URL for our website and base static files URL
    var static_url = site_url + 'static';
    var min_width =100; // minimum width and height in pixels for the images our bookmarklet will try to find on the site
    var min_height = 100;
    function bookmarklet(msg) { // this is main jQuery loader script,it takes care of using jQuery if it has already been loaded on the current website
       //here goes our bookmarklet code
       var css = jQuery('<link>'); // we load the bookmarklet.css stylesheet using a random number as a parameter to prevent the browser from returning a cached file
       css.attr({
         rel: 'stylesheet',
         type: 'text/css',
         href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
       });
       jQuery('head').append(css);

       // load HTML //we add custom html to the document <body> element of the current website,this consists of a <div> element that will contain the images found on the current website
       box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a>
      <h1>Select an image to bookmark:</h1><div class="images"></div></div>';
      jQuery('body').append(box_html);

      // close event // we add an event that removes our html from the document when the user clicks on the close link of our html block,we use the #bookmarklet #close selector to find html element with an id named close,which has a parent element with and ID name bookmarklet
      jQuery('#bookmarklet #close').click(function(){  // jQuery selectors allow you to find html elements,a jQuerys selectors allow you to find HTML elements,a jQuery selector returns all elements found by the given CSS selector
          jQuery('#bookmarklet').remove();
      });
      // find images and display them
      jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) { // we will search all JPEG images displayed on the current website,we iterate over the results using each() method of jQuery
        if (jQuery(image).width() >= min_width && jQuery(image).height() // we add the images with a size larger than the one specified with the min_width and min_height variables to our div class
        >= min_height)
       {
        image_url = jQuery(image).attr('src');
        jQuery('#bookmarklet .images').append('<a href="#"><img src="'+
        image_url +'" /></a>');
       }
    });
    // when an image is selected open URL with it
    jQuery('#bookmarklet .images a').click(function(e){ // we attach click() event to the images link elements
    selected_image = jQuery(this).children('img').attr('src'); // when a user clicks on an image,we set a new variable called selected_image that contains the url of the selected image
    // hide bookmarklet
    jQuery('#bookmarklet').hide(); // hide the bookmarklet and open a new browser window with the URL for bookmarking a new image on our site,we pass the <title> element of the website and the selected image URL as GET parameters
    // open new window to submit the image
    window.open(site_url +'images/create/?url='
                + encodeURIComponent(selected_image)
                + '&title='
                + encodeURIComponent(jQuery('title').text()),
                '_blank');
    });
    };

    // Check if jQuery is loaded
    if(typeof window.jQuery != 'undefined') {  // when jQuery is loaded,it executes bookmarklet() function that will contain our bookmarklet code
        bookmarklet();
    } else {
      // Check for conflicts
      var conflict = typeof window.$ != 'undefined'
      // Create the script and point to Google API
      var script = document.createElement('script');
      script.src = '//ajax.googlepis.com/ajax/libs/jquery/' + jquery_version + '/jquery.min.js'; // if jQuery is not loaded,the script loads jQuery from Google's content delivery network
      // Add the script to the 'head' for processing
      document.head.appendChild(script)
      // create a way to wait untill script loading
      var attempts = 15;
      (function(){
        // Check again if jQuery is undefined
        if(typeof window.jquery == 'undefined') {
         if(--attempts > 0 ) {
           // Calls himself in a few milliseconds
           window.setTimeout(arguments.callee,250)
         } else {
          // Too much attempts to load, send error
          alert('An error ocurred while loading jQuery')
         }
        } else {
            bookmarklet();
        }
      })();
    }

})()

// you will need to be able to load the bookmarklet on any site,including sites served through HTTPS
// django development server is intended only for development and doesn't support HTTPS,to test the bookmarklet over HTTPS,we will use Ngrok,Ngrok is a tool that creates a tunnel to expose your localhost to the internet through HTTP and HTTPS