CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "is_admin" varchar,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO Posts ('user_id', 'category_id', 'title', 'publication_date', 'image_url', 'content','approved') 
VALUES (1, 3, 'how to code', '2024-02-04', 'url.photo', 'coding', 'false');

UPDATE Posts
SET "image_url" = 'https://static.wikia.nocookie.net/pixar/images/7/79/Bookworm.png/12315';


-- Insert sample users
INSERT INTO Users (is_admin,first_name, last_name, email, bio, username, password, profile_image_url, created_on, active) VALUES
('true','John', 'Doe', 'john.doe@example.com', 'A software developer.', 'johndoe', 'password123', 'https://example.com/images/john.jpg', '2024-01-01', 1),
('false','Jane', 'Smith', 'jane.smith@example.com', 'A graphic designer.', 'janesmith', 'password123', 'https://example.com/images/jane.jpg', '2024-01-02', 1),
('false','Alice', 'Johnson', 'alice.johnson@example.com', 'A content writer.', 'alicejohnson', 'password123', 'https://example.com/images/alice.jpg', '2024-01-03', 1),
('true','Bob', 'Brown', 'bob.brown@example.com', 'A project manager.', 'bobbrown', 'password123', 'https://example.com/images/bob.jpg', '2024-01-04', 1);

-- Insert sample categories
INSERT INTO Categories (label) VALUES 
('News'),
('Technology'),
('Lifestyle');

-- Insert sample tags
INSERT INTO Tags (label) VALUES 
('JavaScript'),
('Python'),
('Design');

-- Insert sample reactions
INSERT INTO Reactions (label, image_url) VALUES 
('happy', 'https://example.com/images/happy.png'),
('sad', 'https://example.com/images/sad.png'),
('love', 'https://example.com/images/love.png');

-- Insert sample posts
INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES 
(1, 1, 'How to Code', '2024-02-04', 'https://example.com/images/how_to_code.png', 'This is a post about coding.', 1),
(2, 2, 'Design Trends 2024', '2024-02-05', 'https://example.com/images/design_trends.png', 'This post discusses design trends for 2024.', 1),
(3, 3, 'Healthy Living Tips', '2024-02-06', 'https://example.com/images/healthy_living.png', 'Tips for a healthier lifestyle.', 1),
(4, 1, 'Project Management 101', '2024-02-07', 'https://example.com/images/project_management.png', 'An introduction to project management.', 1);

-- Insert sample subscriptions
INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES 
(1, 2, '2024-01-01'),
(3, 4, '2024-01-02'),
(3, 2, '2024-01-03'),
(1, 3, '2024-01-04'),
(1, 4, '2024-01-05');

-- Insert sample comments
INSERT INTO Comments (post_id, author_id, content) VALUES 
(1, 2, 'Great post! Very informative.'),
(2, 1, 'I love the design tips!'),
(3, 4, 'Thanks for the healthy living tips!'),
(4, 3, 'This is a great introduction to project management.');


-- Insert sample posttags
INSERT INTO PostTags (post_id, tag_id) VALUES 
(1, 1),
(2, 2),
(2, 3),
(4, 1),
(4, 2),
(4, 3);
