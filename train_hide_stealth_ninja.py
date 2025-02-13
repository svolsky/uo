# MUST HAVE REQUIRED NINJA TO ATTEMPT SHADOWJUMP
# best to start in an area between north south trees with visible tiles between

Y_1 = 1334
Y_2 = 1297


def get_direction():
    if Player.Position.Y <= Y_2:
        return 'South'
    elif Player.Position.Y >= Y_1:
        return 'North'
    else:
        return Player.Direction
    

while not Player.IsGhost:   
    if Player.Visible:
        Target.Cancel()        
        Player.UseSkill("Hiding")
        Misc.Pause(3000)
    
    if not Player.Visible:
        dir = get_direction()
        Player.Walk(dir)
        Player.Walk(dir)
        
    if not Player.Visible and Player.Mana > 15: 
        Spells.CastNinjitsu("Shadowjump")
        Target.WaitForTarget(3000, False)
        Target.TargetExecuteRelative(Player.Serial,-1)
        Misc.Pause(3000)
  
    Misc.Pause(400)