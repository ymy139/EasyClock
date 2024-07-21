"""SMTC song info model, tested only on the [InfLink plugin of BetterNCM](https://github.com/BetterNCM/InfinityLink), 
there may be some bugs"""

from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as mediaManger
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionMediaProperties as MediaProperties
from winrt.windows.storage.streams import DataReader

def getSMTCSongInfo() -> dict[str, str] | None:
    """get smtc song info

    Returns:
        dict[str, str]: song info, keys are `artist` and `title`
        None: cannot get smtc song info
    """
    mediaProperties = _getSMTCMediaProperties()
    if mediaProperties == None:
        return None
    artist = mediaProperties.artist.replace(" / ", "/")
    title = mediaProperties.title
    return {"artist": artist, "title": title}
    
def getSMTCSongThumbnailFilePath() -> str | None:
    """get SMTC song thumbnail, write it to file(don't worry, the file will be create in `%TEMP%`), 
    and return file path

    Returns:
        str: file path
        None: cannot get smtc song thumbnail
    """
    mediaProperties = _getSMTCMediaProperties()
    if mediaProperties == None:
        return None
    
    thumbnailStreamReference = mediaProperties.thumbnail
    
    if not thumbnailStreamReference == None:
        thumbnailStream = thumbnailStreamReference.open_read_async().get_results()
        if thumbnailStream == None:
            return None
        
        dataReader = DataReader(thumbnailStream) # type: ignore
        buffer = bytearray(thumbnailStream.size)
        dataReader.load_async(thumbnailStream.size).get_results()
        dataReader.read_bytes(buffer) # type: ignore
        
        thumbnailFile = open("temp/temp.jpg", "wb")
        thumbnailFile.write(buffer)
        thumbnailFile.close()
        
        return "temp/temp.jpg"
    
    return None

def _getSMTCMediaProperties() -> MediaProperties | None:
    """get smtc media properties

    Returns:
        MediaProperties: `GlobalSystemMediaTransportControlsSessionMediaProperties` object
        None: cannot get smtc media properties
    """
    mediaControl = mediaManger.request_async().get_results()
    if mediaControl == None:
        return None
    
    mediaControlsSession = mediaControl.get_current_session()
    if mediaControlsSession == None:
        return None
    
    mediaProperties = mediaControlsSession.try_get_media_properties_async().get_results()
    if mediaProperties == None:
        return None
    
    return mediaProperties