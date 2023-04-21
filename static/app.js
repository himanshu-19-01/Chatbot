class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            hindiButton: document.querySelector('.chatbox__heading--header')
        }
        this.sendmail = false;
        this.hindibtn=false;
        this.state = false;
        this.messages = [];
       
    }

    display() {
        const {openButton, chatBox, sendButton,quaryButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
        console.log("here")
        this.args.hindiButton.addEventListener("click", () => {
            this.hindibtn=true
            const messageElement = chatBox.querySelector(".chatbox__messages");
            const html=('<div class="messages__item messages__item--visitor">नमस्ते , मैं आपकी कैसे सहायता कर सकती हूँ?</div>');
            messageElement.innerHTML += html;
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 } 
        this.messages.push(msg1);
        const payload = { message: text1 ,sendmail: this.sendmail,hindi:this.hindibtn};
        console.log(payload)
        if (this.sendmail) {
        payload.short_query = text1;
        this.sendmail = false;
        }

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify(payload),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            if (r.confirmed) {
                // Handle confirmation logic here
            }
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }
    
    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
             
            if (item.name === "Sam")
            {
                console.log(item.message) 
                if(item.message==="I do not understand If you need any further assist you can just write down your query or contact our customer support team on #9623461271  or if you want to send mail just Tap on 'YES'...") {
                    html += '<div><button class="special-response">YES</button></div>';
                    
                }
                
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
                
                // console.log(item.message) 
            }
            else{
                console.log(item.message)
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
            
            
          });
    
          const chatmessage = chatbox.querySelector('.chatbox__messages');
          chatmessage.innerHTML = html;
      
          const specialResponseBtn = chatmessage.querySelector('.special-response');
          if (specialResponseBtn) {
              specialResponseBtn.addEventListener('click', () => {   
                this.sendmail=true
                console.log('button')
                  this.messages.push({ name: "Sam", message: "Please write your query in short." });
                  this.updateChatText(chatbox);
              });
          }
      }
    }

const chatbox = new Chatbox();
chatbox.display();