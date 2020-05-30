import itertools

class CollisionSystem():
    def __init__(self, game):
        self.character_list = game.character_list
        self.wall_list = game.wall_list
        self.bullet_list = game.bullet_list

    def collided_circle_rect(self, circle, rect):
        circle_dist_x = abs(circle.pos.x - rect.pos.x)
        circle_dist_y = abs(circle.pos.y - rect.pos.y)
        
        if circle_dist_x > rect.width / 2 + circle.radius:
            return False
        if circle_dist_y > rect.height / 2 + circle.radius:
            return False

        if circle_dist_x <= rect.width / 2:
            return True
        if circle_dist_y <= rect.height / 2:
            return True

        corner_distance_sq = (circle_dist_x - rect.width/2)**2 + (circle_dist_y - rect.height/2)**2

        return (corner_distance_sq <= (circle.radius**2))

    def update(self):
        # for x, y in itertools.combinations(self.character_list, 2):
        #     if x.pos.distance_to(y.pos) <= x.radius + y.radius:
        #         collided = True
        # test character-wall collision
        for character in self.character_list:
            for wall in self.wall_list:
                if self.collided_circle_rect(character, wall):
                    character.wall_collision_response()
        # test bullet-wall collision
        for bullet in self.bullet_list:
            for wall in self.wall_list:
                if self.collided_circle_rect(bullet, wall):
                    bullet.wall_collision_response()