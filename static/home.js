// IT is for t1

      var text = "WHAT IS DIGITAL FRAUD ?";
      var firstLetter= text.split("")[0]; // Extracting the first word
      var restOfText = text.substring(firstLetter.length); // Extracting the rest of the text
      var index = 0;
      var speed = 150; // Typing speed in milliseconds
    
      function typeWriter() {
        var element = document.getElementById("t1");
        if (index < restOfText.length) {
          element.innerHTML += restOfText.charAt(index);
          index++;
          setTimeout(typeWriter, speed);
        } else {
          setTimeout(eraseText, 1000); // Wait for 1 second before erasing text
        }
      }
    
      function eraseText() {
        var element = document.getElementById("t1");
        var currentText = element.innerHTML;
        if (currentText.length > firstLetter.length) {
          element.innerHTML = currentText.slice(0, -1); // Erase one character at a time
          setTimeout(eraseText, speed);
        } else if (currentText.length === firstLetter.length) {
          index = 0; // Reset index
          setTimeout(typeWriter, speed); // Start typing animation again
        }
      }
    
      // Call the typing function when the window loads
      window.onload = function() {
        document.getElementById("t1").innerHTML = firstLetter; // Display the first word
        setTimeout(typeWriter, 1000); // Wait for 1 second before typing the rest
      };
   
    // for translator api
    function googleTranslateElementInit() {
      new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
    }
   
    