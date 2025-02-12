# remove traps
# BACKPACK_SERIAL = 

WOODEN_BOX_ID = 0x0E7D
KEYRING_ID    = 0x176B

DOG_ID = 0x00D9

BACKPACK_ID = 0x0E75

USE_PAUSE = 1000


def im_a_dog():
    return Player.MobileID == DOG_ID
    
    
def im_healthy():
    return Player.Hits == Player.HitsMax
    

def heal_as_dog():
    # кастуем собаку и ждем пока не восстановится здоровье
    while not im_a_dog():
        Spells.CastNinjitsu('Animal Form')
        Gumps.WaitForGump(0x2336, 3000)
        Gumps.SendAction(0x2336, 102) # dog
        Misc.Pause(3000)

    print('waiting for full healthbar...')
    while Player.Hits < Player.HitsMax:
        Misc.Pause(3000)
        
    Spells.CastNinjitsu('Animal Form')
    Misc.Pause(3000)
    

    
def get_backpacks():
    backpacks = Items.FindAllByID(BACKPACK_ID, -1, Player.Backpack.Serial, 0)
    return backpacks
        
    
def all_wooden_boxes(backpack):
    # open first
    Items.UseItem(backpack)
    Misc.Pause(USE_PAUSE)
    # ищем wooden box и keyring в сумке
    # все должно лежать в backpack-ах, которые надо открыть
    boxes = Items.FindAllByID(WOODEN_BOX_ID, -1, backpack.Serial, 0)
    
    # keyring
    keyring = Items.FindByID(KEYRING_ID,-1,backpack.Serial,0)
    print(f'keyring: {keyring}')
    return boxes, keyring


def relock_box(box, key):
    Journal.Clear()
    Items.UseItem(key, box)
    Misc.Pause(USE_PAUSE)

    if Journal.Search('You disable the trap'):
        Items.UseItem(key, box)
        Misc.Pause(USE_PAUSE)
        return True
    elif Journal.Search('You re-enable the trap'):
        return True
    else:
        print(f"box don't has trap")
        return False
    
        
        
def remove_trap(box):
    # пытаемся снять ловушку и смотрим по журналу
    while True:
        Journal.Clear()
        Player.UseSkill('Remove Trap')
        Target.WaitForTarget(3000, False)
        Target.TargetExecute(box)
        Misc.Pause(1000)
        
        if Journal.Search("That doesn't appear to be trapped"):
            break
        elif Journal.Search('fail to disarm the trap'):
            Misc.Pause(10000)
        elif Journal.Search('A dart imbeds itself'):
            heal_as_dog()
        elif Journal.Search('You carefully remove'):
            break
        else:
            print('Unexpected outcome')
            
            
    

def train():
    backpacks = get_backpacks()
    for i, backpack in enumerate(backpacks):
        boxes, key = all_wooden_boxes(backpack)
        for box in boxes:
            trapped = relock_box(box, key)
            if trapped:
                remove_trap(box)

            
train()
