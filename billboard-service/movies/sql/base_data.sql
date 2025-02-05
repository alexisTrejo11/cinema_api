-- Cinema inserts (same as before)
INSERT INTO movies_cinema (name, address, phone, email, tax_number, is_active, created_at, updated_at)
VALUES 
    ('Starlight Cinemas', '123 Main Street, Downtown, New York, NY 10001', '+1-212-555-0123', 'info@starlightcinemas.com', 'TAX12345NY', true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),
    ('Royal Movieplex', '456 Park Avenue, Manhattan, NY 10022', '+1-212-555-0124', 'contact@royalmovieplex.com', 'TAX67890NY', true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),
    ('Cinema Paradise', '789 Broadway, Brooklyn, NY 11201', '+1-718-555-0125', 'hello@cinemaparadise.com', 'TAX11223NY', true, '2024-02-05 10:00:00', '2024-02-05 10:00:00');

-- Extended Theater inserts
INSERT INTO movies_theater (cinema_id, name, capacity, theater_type, is_active, maintenance_mode)
VALUES 
    -- Starlight Cinemas (id: 1) theaters
    (1, 'Hall A', 200, '2D', true, false),
    (1, 'Hall B', 180, '3D', true, false),
    (1, 'IMAX Experience', 300, 'IMAX', true, false),
    (1, 'VIP Lounge 1', 40, 'VIP', true, false),
    (1, 'VIP Lounge 2', 40, 'VIP', true, false),
    (1, '4DX Supreme', 120, '4DX', true, false),
    (1, 'Standard Hall 1', 160, '2D', true, false),
    (1, 'Standard Hall 2', 160, '2D', true, false),
    
    -- Royal Movieplex (id: 2) theaters
    (2, 'Screen 1', 150, '2D', true, false),
    (2, 'Screen 2', 150, '3D', true, false),
    (2, 'Screen 3', 150, '2D', true, false),
    (2, 'Screen 4', 150, '3D', true, false),
    (2, '4DX Theater', 100, '4DX', true, false),
    (2, 'IMAX Royal', 280, 'IMAX', true, false),
    (2, 'Premiere Lounge', 50, 'VIP', true, false),
    (2, 'Family Screen', 200, '2D', true, false),
    
    -- Cinema Paradise (id: 3) theaters
    (3, 'VIP Lounge', 50, 'VIP', true, false),
    (3, 'Main Hall', 250, '2D', true, false),
    (3, 'Premium Screen', 200, 'IMAX', true, false),
    (3, 'Paradise 3D-1', 180, '3D', true, false),
    (3, 'Paradise 3D-2', 180, '3D', true, false),
    (3, 'Kids Cinema', 120, '2D', true, false),
    (3, '4DX Paradise', 100, '4DX', true, false),
    (3, 'Couples Lounge', 60, 'VIP', true, false);

-- Extended Movie inserts
INSERT INTO movies_movie (title, original_title, duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active, created_at, updated_at)
VALUES 
    ('The Last Frontier', 'The Last Frontier', 142, '2024-02-01', '2024-04-01', 
    'A gripping sci-fi adventure about humanity''s first interstellar colony mission.', 
    'sci-fi', 'PG-13', 
    'https://example.com/posters/last-frontier.jpg', 
    'https://example.com/trailers/last-frontier.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Love in Paris', 'Amour à Paris', 118, '2024-01-15', '2024-03-15',
    'A heartwarming romantic comedy set in the streets of Paris.',
    'romance', 'PG',
    'https://example.com/posters/love-paris.jpg',
    'https://example.com/trailers/love-paris.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Urban Jungle', 'Urban Jungle', 135, '2024-02-05', '2024-04-05',
    'An action-packed thriller following an elite police unit in a corrupt city.',
    'action', 'R',
    'https://example.com/posters/urban-jungle.jpg',
    'https://example.com/trailers/urban-jungle.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('The Silent Comedy', 'The Silent Comedy', 95, '2024-01-20', '2024-03-20',
    'A modern take on classic silent film comedy with a contemporary twist.',
    'comedy', 'G',
    'https://example.com/posters/silent-comedy.jpg',
    'https://example.com/trailers/silent-comedy.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Quantum Paradox', 'Quantum Paradox', 155, '2024-02-10', '2024-04-10',
    'A mind-bending science fiction thriller about time travel and parallel universes.',
    'sci-fi', 'PG-13',
    'https://example.com/posters/quantum-paradox.jpg',
    'https://example.com/trailers/quantum-paradox.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('The Hidden Truth', 'The Hidden Truth', 128, '2024-02-08', '2024-04-08',
    'A gripping drama about investigative journalists uncovering a corporate scandal.',
    'drama', 'PG-13',
    'https://example.com/posters/hidden-truth.jpg',
    'https://example.com/trailers/hidden-truth.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Dance of Dreams', 'Dance of Dreams', 112, '2024-01-25', '2024-03-25',
    'A touching drama about a young ballet dancer pursuing her dreams against all odds.',
    'drama', 'PG',
    'https://example.com/posters/dance-dreams.jpg',
    'https://example.com/trailers/dance-dreams.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Midnight Chase', 'Midnight Chase', 138, '2024-02-15', '2024-04-15',
    'A high-stakes thriller about a night of cat-and-mouse through city streets.',
    'thriller', 'R',
    'https://example.com/posters/midnight-chase.jpg',
    'https://example.com/trailers/midnight-chase.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Family Reunion', 'Family Reunion', 105, '2024-01-30', '2024-03-30',
    'A hilarious comedy about three generations coming together for a weekend.',
    'comedy', 'PG',
    'https://example.com/posters/family-reunion.jpg',
    'https://example.com/trailers/family-reunion.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('The Last Guardian', 'The Last Guardian', 162, '2024-02-20', '2024-04-20',
    'An epic fantasy adventure about protecting an ancient magical realm.',
    'action', 'PG-13',
    'https://example.com/posters/last-guardian.jpg',
    'https://example.com/trailers/last-guardian.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Sweet Summer Romance', 'Sweet Summer Romance', 98, '2024-02-12', '2024-04-12',
    'A charming romantic comedy set during a beach town''s summer festival.',
    'romance', 'PG',
    'https://example.com/posters/summer-romance.jpg',
    'https://example.com/trailers/summer-romance.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00'),

    ('Tech Revolution', 'Tech Revolution', 145, '2024-02-18', '2024-04-18',
    'A dramatic look at the rise and fall of a revolutionary tech startup.',
    'drama', 'PG-13',
    'https://example.com/posters/tech-revolution.jpg',
    'https://example.com/trailers/tech-revolution.mp4',
    true, '2024-02-05 10:00:00', '2024-02-05 10:00:00');