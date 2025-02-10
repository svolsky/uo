# type of stealable
ITEM_ID = 0x097A
# packtorse to steal from
PACKHORSE_SERIAL = 0x0175967A


# at beginning of script packhorse must be empty and stay near

# do some calcs: items weight must be stealing / 10
# i.e. stealing = 46.1 weight must be 4
# пока расчеты не делаем. просто константа
def get_items_amount():
    # 10 steaks = 1 stone
    stealing = Player.GetSkillValue('Stealing')
    if stealing < 60:
        return 50
    elif stealing < 70:
        return 60
    elif stealing < 80:
        return 70
    elif stealing < 90:
        return 80
    else:
        return 90


def grab_all_from_packhorse():
    packhorse = Mobiles.FindBySerial(PACKHORSE_SERIAL)
    #print(f'Backpack: {packhorse.Backpack}')
    items = Items.FindAllByID(ITEM_ID, -1, packhorse.Backpack.Serial, 0)
    for item in items:
        Items.Move(item, Player.Backpack, item.Amount)
        Misc.Pause(1000)
    

# move some of items to packhorse
def move_items_to_packhorse():
    # находим все пачки и проверяем сколько там
    items = Items.FindAllByID(ITEM_ID, -1, Player.Backpack.Serial, 0)
    amount = get_items_amount()

    for item in items:
        # тут надо чтобы было больше. чтобы был другой айди айтема
        if item.Amount > amount:
            Items.Move(item, PACKHORSE_SERIAL, amount)
        else:
            # place to backpack to stack
            Items.Move(item, Player.Backpack.Serial, item.Amount)
        Misc.Pause(1000)
    

def steal_item():
    packhorse = Mobiles.FindBySerial(PACKHORSE_SERIAL)
    
    items = Items.FindAllByID(ITEM_ID, -1, packhorse.Backpack.Serial, 0)
    for item in items:
        print(f'trying to steal {item}')
        Player.UseSkill('Stealing')
        Target.WaitForTarget(3000, False)
        Target.TargetExecute(item)
        Misc.Pause(10000)
    
    
while True:
    grab_all_from_packhorse()
                
    move_items_to_packhorse()

    steal_item()
