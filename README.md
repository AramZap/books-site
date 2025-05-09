# 🚀 Final Project Submission

## ✅ Submission Requirements

1. **GitHub Repository Link**  
   Paste the public link to your code repository here:  
   `https://github.com/AramZap/books-site`

2. **Hosted Website Link**  
   Provide the URL to your deployed/hosted website here:  
   `https://books-site-beta.vercel.app`

3. **Final Write-up**  
   Our write-up is below in markdown

4. **Initial Proposal**
   Here is a link to a Google Doc of our initial proposal:
   `https://docs.google.com/document/d/1ctM2ys3kXTbVojGMX22jJczsfpAG9ks5JPml8UcIrok/edit?usp=sharing`

   ---
   ### 📝 Final Write-up

   #### Project Title: Book Tracker

   **Team Members:**  
   - Aram Zaprosyan
   - Trenton Regis 
   - Maurice Barksdale
   - Aryan Thakar
   - Syed Ahmed


   **Overview:**  
   Book Tracker is a website where users can keep track of books they have read by adding books to their collection as well as their ratings and notes regarding each book. They can also view their collections and edit the ratings/notes they have given to any of their books!


   **Registration and Login:**  
   Only logged-in users can add books to their collection, see their collection, and add ratings and notes of their books. Additionally, only a logged-in user can edit details of their account - edit their username and add/change their profile picture.


   **Forms:**  
   - Registration: user needs an email address, name, and password to register an account
   - Login: user needs to enter a valid email address and password to log in to their account
   - AddBook: after a user has selected a book to add to their collection, they must give the book a rating(out of 5) and any notes about the book to add a book to their collection
   - Search: user can search for any book by title - which queries the OpenLibrary API through our website
   - ModifyBook: after selecting a book in their collection, a user can modify the notes they wrote about the book as well as the rating they gave the book
   - UpdateUsername: user can change their username to one that isn't claimed by another user
   - UpdateProfilePic: user can add or change their profile picture


   **Blueprints and Routes for each:**  

    ### Users - User control and management including account information

    **Routes:**
    - Register – Make an account  
    - Log in – Log in to an account  
    - Log out – Log out of that account  
    - Account – Display information about account and can change details  

    ### Books – Information about users’ book collections, adding books, and adding/editing notes/ratings

    **Routes:**
    - Index - provides buttons to view collection 
    - **Collection** – View books you have added  
    - **Add Book** – Add a new book  
    - **Review** – Leave reviews/comments on books you have added  


   **Database:**
   - Information pertaining to user accounts - email, usernames, passwords, and profile pictures
   - Information pertaining to each user’s book collection - info about books they have added: book cover images, author images, book title, date the book was added/modified in their collection, publication year, author's name, and users’ ratings and notes of the books they have added.

  
   **API:**
    This is the API we will use: https://openlibrary.org/developers/api
    It allows us to get information about a book from its title or ISBN. This includes getting images corresponding to cover pages of these books. This will affect the user experience by making it easier for users to add books to their collections since they only need to add in the titles and the website takes care of the rest, including the cover pages to present back to them. We also use the API to get images of the authors of books to present to the user as it is nice to be able to see the authors of books your read since people tend to not see photos of their book's authors anywhere!


   ---