# lumber

HATCHET_ID = 0x0F43

LOGS_ID = 0x1BDD


def axe_equipped():
    item = Player.GetItemOnLayer('LeftHand')
    if item and item.Name == 'hatchet':
        return True
    return False
    
    

def take_axe():
    if axe_equipped():
        return
    
    axe = Items.FindByID(HATCHET_ID, -1, Player.Backpack.Serial)
    print(f'found: {axe}')
    if axe:
        Player.EquipItem(axe)
        Misc.Pause(500)


def logs_to_boards(axe):
    if Player.Weight >= Player.MaxWeight * 0.95:
        logs = Items.FindAllByID(LOGS_ID, -1, Player.Backpack.Serial, -1)
            
        for log in logs:
            Items.UseItem(axe)
            Target.WaitForTarget(5000, False)
            Target.TargetExecute(log)
            Misc.Pause(1000)
        
    # return true if can continue chopping
    return Player.Weight < Player.MaxWeight * 0.95
        
    
def chop_tree():
    Journal.Clear()
    wood_to_chop = True
    while wood_to_chop:
        # chop
        axe = Player.GetItemOnLayer("LeftHand")
        Target.TargetResource(axe, "wood")
        
        # wait for result to check journal
        Misc.Pause(1000)
        
        if Journal.Search("not enough wood here"):
            print("Stopping due to finished")
            wood_to_chop = False
        if Journal.Search("put item into your backpack"):
            Misc.Pause(2000)
        if Journal.Search("fail to produce"):
            Misc.Pause(2000)

        
        can_continue = logs_to_boards(axe)
        if not can_continue:
            print('Stop due to overweight')
            return
        
            
    
take_axe()

chop_tree()