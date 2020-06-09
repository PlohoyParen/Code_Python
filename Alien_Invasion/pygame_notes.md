# pygame
Некоторые пояснения

### Surface
Все картинки (включая основной фон) - это surface. Каждая surface имеет позицию, которая задается через метод `.rect` - это позиция. 
- `surface.get_rect()` - задает размеры объекта
- Позиция объекта считается по верхнему левому углу картинки. Позиции задаются через x и y координаты: `surface.center`- центр поверхности, `.centerx`- центр по x, `.centery` - центр по y. Также `.top`, `.bottom`, `.left` и `.right` задают позицию относительно экрана (главной поверхности). `surface.rect.right` - это правая (`.left` - левая) граница поверхности. `.rect.width` - дает полную ширину объекта.
- Начальная позиция экрана (0,0) - это верхний левый угол. Если разрешение экрана задано через (1200, 800), то экран разбивается на 1200 по x и 800 по y, а правый нижний угол - это (1200, 800).
- `pygame.draw.rect(screen, color, rect)` function fills the part of the screen 
defined by the surface rect with the color.
### Events
Event в pygame - это любое нажатие клавиши на клавиатуре и/или мыши 
`pygame.event.get()` - срачитывает эти events
Через цикл "раскурчиваются" все наблюдаемые events. Потом ветвлением опаределяется
 тип и соответствующее повидение программы.
```
for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
```
### Sprites
Позволят управлять сразу группой однотипных объектов. Там есть два класса: 
**Sprite** и **Group**. **Spite** - это единственный объект и обычно из него унаследуют
конкретные кастомные объекты. **Group** - это специальный класс, который собирает
 в себя спрайты, создает из них список и предоставляет операции над всем списком сразу.
`from pygame.sprite import Group`
- `Group.sprites()`-  method returns a list of all sprites in the group 

####sprite.groupcollide()
`collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)`
method compares each bullet’s rect with each alien’s rect and returns a dictionary containing the bullets and aliens that have collided. Each key in the dictionary is a bullet, and the corresponding value is the alien that was hit.
`(..,True, True)` - указывает, удалять ли объекты в случаи их collision (True)