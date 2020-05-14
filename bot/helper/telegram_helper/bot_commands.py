class _BotCommands:
    def __init__(self):
        self.StartCommand = 'st'
        self.MirrorCommand = 'de'
        self.TarMirrorCommand = 'demirror'
        self.CancelMirror = 'snap'
        self.CancelAllCommand = 'snapall'
        self.ListCommand = 'list'
        self.StatusCommand = 'status'
        self.AuthorizeCommand = 'authorize'
        self.UnAuthorizeCommand = 'unauthorize'
        self.PingCommand = 'ping'
        self.RestartCommand = 'restart'
        self.StatsCommand = 'stats'
        self.HelpCommand = 'help'
        self.LogCommand = 'log'
        self.CloneCommand = "copy"
        self.WatchCommand = 'w'
        self.TarWatchCommand = 'wtar'

BotCommands = _BotCommands()
